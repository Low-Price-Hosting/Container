#!/usr/bin/env python3
"""Discover production targets from the organization's source snapshots."""
import argparse
import concurrent.futures
import hashlib
import importlib.util
import json
import os
import pathlib
import re
import subprocess
import tempfile

REPO_ROOT = pathlib.Path(__file__).resolve().parent.parent
spec = importlib.util.spec_from_file_location('repository_metadata', REPO_ROOT / 'scripts/repository-metadata.py')
metadata = importlib.util.module_from_spec(spec)
spec.loader.exec_module(metadata)

DISTRIBUTIONS = ('Ubuntu', 'Debian', 'Centos', 'Alpine', 'Fedora', 'AlmaLinux', 'ArchLinux', 'RockyLinux')


def command(*args):
    return subprocess.check_output(args, text=True).strip()


def platforms(bootstrap):
    manifest = json.loads(command('docker', 'buildx', 'imagetools', 'inspect', '--raw', bootstrap))
    result = {}
    for item in manifest.get('manifests', []):
        p = item.get('platform', {})
        if (p.get('os') != 'linux' or p.get('architecture') in (None, '', 'unknown')
                or item.get('annotations', {}).get('vnd.docker.reference.type') == 'attestation-manifest'):
            continue
        variant = p.get('variant', '')
        # arm64/v8 is the default arm64 platform supported by native runners.
        if p['architecture'] == 'arm64' and variant == 'v8':
            variant = ''
        result['linux/' + p['architecture'] + (('/' + variant) if variant else '')] = item['digest']
    if not result:
        raise RuntimeError(f'{bootstrap} does not advertise supported build architectures')
    return dict(sorted(result.items()))


def files_hash(root, paths):
    digest = hashlib.sha256()
    for path in sorted(paths):
        relative = path.relative_to(root).as_posix()
        data = path.read_bytes()
        if b'\0' not in data:
            data = data.replace(b'\r\n', b'\n')
        digest.update(relative.encode() + b'\0' + data + b'\0')
    return digest.hexdigest()


def recipe_hash(distribution, version, source):
    paths = [p for p in source.rglob('*') if p.is_file() and '.git' not in p.relative_to(source).parts
             and not p.name.startswith(('.container-', 'README', 'LICENSE', 'COPYING'))]
    if distribution == 'AlmaLinux':
        paths = [source / 'Containerfiles' / version / 'Containerfile.default']
    elif distribution == 'Centos':
        paths = [p for p in paths if p.name.startswith(f'CentOS-Stream-{version.removeprefix("stream")}-')]
    return files_hash(source, paths)


def implementation_hash(distribution):
    lower = distribution.lower()
    paths = ['build-base.sh', 'scripts/build-common.sh', 'scripts/package-cache.sh', 'scripts/test-images.sh']
    if distribution in ('Centos', 'RockyLinux'):
        paths.append('scripts/kickstart-rootfs.py')
    if distribution in ('Fedora', 'RockyLinux'):
        paths.append('scripts/label-oci.py')
    files = [REPO_ROOT / path for path in paths]
    files += [p for p in (REPO_ROOT / lower).rglob('*') if p.is_file()]
    return files_hash(REPO_ROOT, files)


def tested_record(target):
    # The full input hash is part of the tag: Docker manifest lists discard OCI annotations.
    reference = ('ghcr.io/low-price-hosting/' + target['distribution'].lower()
                 + ':tested-' + target['key'] + '-sha' + target['fingerprint'])
    inspect = subprocess.run(['docker', 'buildx', 'imagetools', 'inspect', '--format', '{{json .}}', reference],
                             text=True, capture_output=True)
    if inspect.returncode:
        return None
    manifest = json.loads(inspect.stdout)['manifest']
    platforms_found = set()
    for item in manifest.get('manifests', []):
        p = item.get('platform', {})
        if p.get('os') == 'linux':
            variant = p.get('variant', '')
            if p['architecture'] == 'arm64' and variant == 'v8':
                variant = ''
            platforms_found.add('linux/' + p['architecture'] + ('/' + variant if variant else ''))
    if platforms_found != {target['platform']}:
        return None
    return dict(key=target['key'], platform=target['platform'], fingerprint=target['fingerprint'],
                tested=True, pushed=True, image=reference.split(':')[0] + '@' + manifest['digest'])


def release_published(targets):
    images = sorted(target['reused']['image'] for target in targets)
    digest = hashlib.sha256('\n'.join(images).encode()).hexdigest()[:16]
    repository = 'ghcr.io/low-price-hosting/' + targets[0]['distribution'].lower()
    expected = subprocess.run(['docker', 'buildx', 'imagetools', 'inspect', '--format', '{{json .Manifest}}',
                               repository + ':' + targets[0]['version'] + '-build' + digest],
                              text=True, capture_output=True)
    if expected.returncode:
        return False
    expected_digest = json.loads(expected.stdout)['digest']
    tags = {targets[0]['version'], *(alias for target in targets for alias in target['aliases'])}
    for tag in sorted(tags):
        inspect = subprocess.run(['docker', 'buildx', 'imagetools', 'inspect', '--format', '{{json .Manifest}}',
                                  repository + ':' + tag], text=True, capture_output=True)
        if inspect.returncode:
            return False
        manifest = json.loads(inspect.stdout)
        if manifest['digest'] != expected_digest:
            return False
    return True


def release_matrix(plan, verify_only=False):
    groups = {}
    for target in plan['include']:
        groups.setdefault((target['distribution'], target['version']), []).append(target)
    for error in plan.get('errors', []):
        groups.setdefault((error['distribution'], error.get('version', 'sources')), [])
    releases = []
    for (distribution, version), targets in sorted(groups.items()):
        changed = [target for target in targets if not target.get('reused') and not target.get('error')]
        errors = [error for error in plan.get('errors', []) if error['distribution'] == distribution
                  and error.get('version', 'sources') == version]
        has_errors = bool(errors) or any(target.get('error') for target in targets)
        if not changed and not has_errors and (verify_only or release_published(targets)):
            continue
        releases.append(dict(distribution=distribution, version=version,
                             key=distribution.lower() + '-' + version, targets=changed,
                             has_changes=bool(changed), has_errors=has_errors))
    return {'include': releases}


def plan_target(target, source, verify_only):
    try:
        packages = metadata.fingerprint(target, source, REPO_ROOT)
        inputs = [recipe_hash(target['distribution'], target['version'], source),
                  implementation_hash(target['distribution']), target['bootstrap'], target['platform'],
                  target['version'], packages]
        target['fingerprint'] = hashlib.sha256(json.dumps(inputs).encode()).hexdigest()
        if not verify_only:
            target['reused'] = tested_record(target)
    except Exception as error:
        target['error'] = str(error)
    return target


def targets(distribution, source, branches):
    releases = json.loads((source / '.container-releases.json').read_text())
    if distribution == 'Centos':
        for ks in source.glob('CentOS-Stream-*-container-base.ks'):
            major = re.fullmatch(r'CentOS-Stream-(\d+)-container-base.ks', ks.name)[1]
            releases.append(dict(version='stream' + major, branch='main',
                                 bootstrap=f'quay.io/centos/centos:stream{major}', aliases=[]))
    elif distribution == 'AlmaLinux':
        for recipe in (source / 'Containerfiles').glob('*/Containerfile.default'):
            if recipe.parent.name.isdecimal():
                major = recipe.parent.name
                releases.append(dict(version=major, branch='main',
                                     bootstrap=f'quay.io/almalinuxorg/almalinux:{major}', aliases=[]))
    elif distribution == 'RockyLinux':
        for branch in branches:
            if re.fullmatch(r'r\d+', branch):
                major = branch[1:]
                releases.append(dict(version=major, branch=branch,
                                     bootstrap=f'quay.io/rockylinux/rockylinux:{major}', aliases=[]))
    elif distribution == 'ArchLinux':
        releases.append(dict(version='rolling', branch='main',
                             bootstrap='docker.io/library/archlinux:base', aliases=['latest', 'base']))
    if not releases:
        raise RuntimeError(f'No production recipes discovered for {distribution}')
    if distribution in ('Centos', 'AlmaLinux', 'RockyLinux'):
        latest = max(releases, key=lambda r: int(r['version'].removeprefix('stream')))
        latest['aliases'].append('latest')
    return releases


def source_catalog(distribution, source):
    mirror = f'https://github.com/Low-Price-Hosting/{distribution}.git'
    subprocess.run(['git', 'clone', '--quiet', '--depth=1', '--single-branch', '--branch=main',
                    mirror, str(source)], check=True)
    provenance = json.loads((source / '.container-source.json').read_text())
    if provenance.get('schema') != 1 or provenance.get('distribution') != distribution:
        raise RuntimeError(f'{distribution} is not a production-code snapshot; run Cron first')
    refs = command('git', 'ls-remote', '--heads', mirror).splitlines()
    branches = {line.split('refs/heads/', 1)[1] for line in refs}
    return branches, targets(distribution, source, branches)


def release_job_id(distribution, version):
    return 'Build_' + distribution + '_' + re.sub(r'[^A-Za-z0-9_]', '_', version)


def discover(selected='all', version='all', verify_only=False):
    result = []
    errors = []
    with tempfile.TemporaryDirectory(prefix='container-discovery-') as temp:
        for distribution in DISTRIBUTIONS:
            if selected not in ('all', distribution):
                continue
            mirror = f'https://github.com/Low-Price-Hosting/{distribution}.git'
            source = pathlib.Path(temp) / distribution
            try:
                branches, releases = source_catalog(distribution, source)
            except Exception as error:
                errors.append(dict(distribution=distribution, error=str(error)))
                continue
            snapshots = {'main': source}
            for release in releases:
                if version != 'all' and release['version'] != version:
                    continue
                try:
                    if release['branch'] not in branches:
                        raise RuntimeError(f"Missing source branch: {distribution}/{release['branch']}")
                    if release['branch'] not in snapshots:
                        snapshot = source.parent / (distribution + '-' + release['branch'].replace('/', '-'))
                        subprocess.run(['git', 'clone', '--quiet', '--depth=1', '--single-branch',
                                        '--branch=' + release['branch'], mirror, str(snapshot)], check=True)
                        snapshots[release['branch']] = snapshot
                    snapshot = snapshots[release['branch']]
                    commit = command('git', '-C', str(snapshot), 'rev-parse', 'HEAD')
                    available = platforms(release['bootstrap'])
                except Exception as error:
                    errors.append(dict(distribution=distribution, version=release['version'], error=str(error)))
                    continue
                pending = []
                for platform in available:
                    key = '-'.join([distribution.lower(), release['version'], platform.replace('/', '-')])
                    arch = platform.split('/')[1]
                    pinned_release = dict(release, bootstrap=release['bootstrap'].split('@')[0] + '@' + available[platform])
                    pending.append(dict(distribution=distribution, **pinned_release, platform=platform, key=key,
                                        source_commit=commit,
                                        emulation=arch if arch not in ('amd64', 'arm64', '386') else '',
                                        runner='ubuntu-24.04-arm' if arch == 'arm64' else 'ubuntu-24.04'))
                with concurrent.futures.ThreadPoolExecutor(max_workers=6) as pool:
                    result += list(pool.map(lambda t: plan_target(t, snapshot, verify_only), pending))
    if not result and not errors:
        raise RuntimeError('No build targets matched the request')
    changed = [t for t in result if not t.get('reused') and not t.get('error')]
    return dict(include=result, matrix={'include': changed}, errors=errors)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--distribution', choices=('all', *DISTRIBUTIONS), default='all')
    parser.add_argument('--version', default='all')
    parser.add_argument('--verify-only', action='store_true')
    args = parser.parse_args()
    plan = discover(args.distribution, args.version, args.verify_only)
    plan['releases'] = release_matrix(plan, args.verify_only)
    output = os.environ.get('GITHUB_OUTPUT')
    if output:
        with open(output, 'a') as stream:
            releases = {release_job_id(r['distribution'], r['version']): r
                        for r in plan['releases']['include'] if r['version'] != 'sources'}
            stream.write('releases=' + json.dumps(releases, separators=(',', ':')) + '\n')
            stream.write('has_source_errors=' + str(any('version' not in e for e in plan['errors'])).lower() + '\n')
    summary = os.environ.get('GITHUB_STEP_SUMMARY')
    if summary:
        with open(summary, 'a') as stream:
            stream.write('## Build plan\n\n| Distribution / release | Platform | Decision |\n|---|---|---|\n')
            for target in plan['include']:
                state = ('Failed: ' + target['error'].replace('|', '\\|').replace('\n', ' ')) if target.get('error') else 'Reuse tested image' if target.get('reused') else 'Build and test'
                stream.write(f"| {target['distribution']} {target['version']} | {target['platform']} | {state} |\n")
            for error in plan['errors']:
                stream.write(f"\n**{error['distribution']} {error.get('version', '')}:** {error['error']}\n")
    print(json.dumps(plan, separators=(',', ':')))
