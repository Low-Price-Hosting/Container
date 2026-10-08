#!/usr/bin/env python3
"""Discover production targets from the organization's source snapshots."""
import argparse
import concurrent.futures
import functools
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
spec = importlib.util.spec_from_file_location('publication', REPO_ROOT / 'scripts/publish-manifests.py')
publication = importlib.util.module_from_spec(spec)
spec.loader.exec_module(publication)

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


def descriptor_platform(item):
    platform = item.get('platform', {})
    architecture = platform.get('architecture')
    if platform.get('os') != 'linux' or not architecture or architecture == 'unknown':
        return None
    variant = platform.get('variant', '')
    return 'linux/' + architecture + ('/' + variant if variant else '')


@functools.lru_cache(maxsize=256)
def registry_digest(reference):
    inspect = subprocess.run(['docker', 'buildx', 'imagetools', 'inspect', '--format',
                              '{{.Manifest.Digest}}', reference], text=True, capture_output=True)
    digest = inspect.stdout.strip()
    return digest if not inspect.returncode and re.fullmatch(r'sha256:[a-f0-9]{64}', digest) else None


@functools.lru_cache(maxsize=128)
def published_index(reference):
    digest = registry_digest(reference)
    if not digest:
        return None
    # Read the immutable digest so a simultaneous alias update cannot mix two indexes.
    repository = reference.split(':', 1)[0]
    inspect = subprocess.run(['docker', 'buildx', 'imagetools', 'inspect', '--raw',
                              repository + '@' + digest], text=True, capture_output=True)
    if inspect.returncode:
        return None
    try:
        index = json.loads(inspect.stdout)
    except (json.JSONDecodeError, TypeError):
        return None
    if (not isinstance(index, dict) or index.get('schemaVersion') != 2
            or index.get('mediaType') != 'application/vnd.oci.image.index.v1+json'
            or not isinstance(index.get('manifests'), list)):
        return None
    return digest, index


def tested_record(target):
    repository = 'ghcr.io/low-price-hosting/' + target['distribution'].lower()
    published = published_index(repository + ':' + target['version'])
    if not published or not re.fullmatch(r'[a-f0-9]{64}', target.get('fingerprint', '')):
        return None
    _, index = published
    matching = [item for item in index['manifests']
                if descriptor_platform(item) == target['platform']]
    # A duplicated architecture or a partial fingerprint is never a tested cache hit.
    if len(matching) != 1:
        return None
    descriptor = matching[0]
    annotations = descriptor.get('annotations', {})
    if (annotations.get('io.low-price-hosting.build.inputs') != target['fingerprint']
            or annotations.get('io.low-price-hosting.tested') != 'true'
            or not re.fullmatch(r'sha256:[a-f0-9]{64}', descriptor.get('digest', ''))
            or descriptor.get('mediaType') not in ('application/vnd.oci.image.manifest.v1+json',
                                                   'application/vnd.docker.distribution.manifest.v2+json')
            or not isinstance(descriptor.get('size'), int) or descriptor['size'] <= 0):
        return None
    record = dict(key=target['key'], platform=target['platform'], fingerprint=target['fingerprint'],
                  tested=True, pushed=True, image=repository + '@' + descriptor['digest'],
                  descriptor=descriptor)
    if annotations.get('io.low-price-hosting.os.version'):
        record['os_version'] = annotations['io.low-price-hosting.os.version']
    return record


def release_published(targets):
    if not targets or any(not target.get('reused') for target in targets):
        return False
    images = sorted(target['reused']['image'] for target in targets)
    inputs = hashlib.sha256('\n'.join(images).encode()).hexdigest()
    repository = 'ghcr.io/low-price-hosting/' + targets[0]['distribution'].lower()
    version = targets[0]['version']
    published = published_index(repository + ':' + version)
    if not published:
        return False
    expected_digest, index = published
    annotations = index.get('annotations', {})
    expected_metadata = {
        'io.low-price-hosting.release.schema': '2',
        'io.low-price-hosting.release.inputs': inputs,
        'org.opencontainers.image.source': 'https://github.com/Low-Price-Hosting/' + targets[0]['distribution'],
        'org.opencontainers.image.title': targets[0]['distribution'] + ' ' + version,
        'org.opencontainers.image.version': version,
        'io.low-price-hosting.build.source': 'https://github.com/Low-Price-Hosting/Container',
    }
    if (any(annotations.get(key) != value for key, value in expected_metadata.items())
            or not isinstance(annotations.get('org.opencontainers.image.description'), str)
            or not annotations['org.opencontainers.image.description'].strip()):
        return False
    wanted = {target['platform']: target for target in targets}
    descriptors = index['manifests']
    if len(wanted) != len(targets) or len(descriptors) != len(wanted):
        return False
    found = set()
    for descriptor in descriptors:
        platform = descriptor_platform(descriptor)
        if platform not in wanted or platform in found:
            return False
        found.add(platform)
        target = wanted[platform]
        metadata = descriptor.get('annotations', {})
        if (metadata.get('io.low-price-hosting.build.inputs') != target['fingerprint']
                or metadata.get('io.low-price-hosting.tested') != 'true'
                or repository + '@' + descriptor.get('digest', '') != target['reused']['image']):
            return False
    tags = {version, *(alias for target in targets for alias in target['aliases'])}
    os_versions = {target['reused'].get('os_version') for target in targets}
    if len(os_versions) == 1:
        os_version = os_versions.pop()
        if os_version and re.fullmatch(r'[A-Za-z0-9][A-Za-z0-9._-]*', os_version):
            tags.add(os_version)
    docker_repository = 'docker.io/lphllc/' + targets[0]['distribution'].lower()
    quay_repository = publication.quay_repository(targets[0]['distribution'])
    # Backfill registries from immutable, tested GHCR records when indexes or aliases
    # are missing/outdated. This queues publication without rebuilding unchanged images.
    return all(registry_digest(destination + ':' + tag) == expected_digest
               for destination in (repository, docker_repository, quay_repository) for tag in sorted(tags))


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
                                        architecture=platform.removeprefix('linux/'),
                                        source_commit=commit,
                                        emulation=arch if arch not in ('amd64', 'arm64', '386') else '',
                                        runner='ubuntu-24.04-arm' if arch == 'arm64' else 'ubuntu-24.04'))
                with concurrent.futures.ThreadPoolExecutor(max_workers=6) as pool:
                    result += list(pool.map(lambda t: plan_target(t, snapshot, verify_only), pending))
    if not result and not errors:
        raise RuntimeError('No build targets matched the request')
    changed = [t for t in result if not t.get('reused') and not t.get('error')]
    return dict(include=result, matrix={'include': changed}, errors=errors)


def workflow_outputs(plan):
    """Create build and release matrices directly from this run's discovery."""
    releases = [r for r in plan['releases']['include'] if r['version'] != 'sources']
    targets = [target for release in releases for target in release['targets']]
    output = os.environ.get('GITHUB_OUTPUT')
    if output:
        with open(output, 'a') as stream:
            for name, value in (('targets', dict(include=targets)), ('has-builds', bool(targets)),
                                ('releases', dict(include=releases)), ('has-releases', bool(releases))):
                stream.write(f'{name}={json.dumps(value, separators=(",", ":"))}\n')


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--distribution', choices=('all', *DISTRIBUTIONS), default='all')
    parser.add_argument('--version', default='all')
    parser.add_argument('--verify-only', action='store_true')
    args = parser.parse_args()
    plan = discover(args.distribution, args.version, args.verify_only)
    plan['releases'] = release_matrix(plan, args.verify_only)
    plan['verify_only'] = args.verify_only
    workflow_outputs(plan)
    print(json.dumps(plan, separators=(',', ':')))
