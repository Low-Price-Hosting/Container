#!/usr/bin/env python3
"""Discover production targets from the organization's source snapshots."""
import argparse
import json
import pathlib
import re
import subprocess
import tempfile

DISTRIBUTIONS = ('Ubuntu', 'Debian', 'Centos', 'Alpine', 'Fedora', 'AlmaLinux', 'ArchLinux', 'RockyLinux')
SUPPORTED_ARCHES = {'amd64', 'arm64', '386', 'arm', 'ppc64le', 's390x', 'riscv64'}


def command(*args):
    return subprocess.check_output(args, text=True).strip()


def platforms(bootstrap):
    manifest = json.loads(command('docker', 'buildx', 'imagetools', 'inspect', '--raw', bootstrap))
    result = set()
    for item in manifest.get('manifests', []):
        p = item.get('platform', {})
        if p.get('os') != 'linux' or p.get('architecture') not in SUPPORTED_ARCHES:
            continue
        variant = p.get('variant', '')
        if p['architecture'] == 'arm' and variant not in ('v6', 'v7'):
            continue
        # arm64/v8 is the default arm64 platform supported by native runners.
        if p['architecture'] == 'arm64' and variant == 'v8':
            variant = ''
        result.add('linux/' + p['architecture'] + (('/' + variant) if variant else ''))
    if not result:
        raise RuntimeError(f'{bootstrap} does not advertise supported build architectures')
    return sorted(result)


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


def discover(selected='all', architecture='all', version='all'):
    result = []
    with tempfile.TemporaryDirectory(prefix='container-discovery-') as temp:
        for distribution in DISTRIBUTIONS:
            if selected not in ('all', distribution):
                continue
            mirror = f'https://github.com/Low-Price-Hosting/{distribution}.git'
            source = pathlib.Path(temp) / distribution
            subprocess.run(['git', 'clone', '--quiet', '--depth=1', '--single-branch', '--branch=main',
                            mirror, str(source)], check=True)
            provenance = json.loads((source / '.container-source.json').read_text())
            if provenance.get('schema') != 1 or provenance.get('distribution') != distribution:
                raise RuntimeError(f'{distribution} is not a production-code snapshot; run Cron first')
            refs = command('git', 'ls-remote', '--heads', mirror).splitlines()
            branches = {line.split('refs/heads/', 1)[1] for line in refs}
            for release in targets(distribution, source, branches):
                if version != 'all' and release['version'] != version:
                    continue
                if release['branch'] not in branches:
                    raise RuntimeError(f"Missing source branch: {distribution}/{release['branch']}")
                # No architecture is inferred from another distribution's image.
                available = ['linux/amd64'] if distribution == 'ArchLinux' else platforms(release['bootstrap'])
                for platform in available:
                    if architecture != 'all' and platform.split('/')[1] != architecture:
                        continue
                    key = '-'.join([distribution.lower(), release['version'], platform.replace('/', '-')])
                    result.append(dict(distribution=distribution, **release, platform=platform, key=key,
                                       runner='ubuntu-24.04-arm' if platform.startswith('linux/arm64') else 'ubuntu-24.04'))
    if not result:
        raise RuntimeError('No build targets matched the request')
    if len(result) > 256:
        raise RuntimeError('The discovered targets exceed GitHub Actions matrix capacity')
    return {'include': result}


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--distribution', choices=('all', *DISTRIBUTIONS), default='all')
    parser.add_argument('--architecture', default='all')
    parser.add_argument('--version', default='all')
    args = parser.parse_args()
    print(json.dumps(discover(args.distribution, args.architecture, args.version), separators=(',', ':')))
