#!/usr/bin/env python3
"""Check official package indexes without starting a target-architecture builder."""
import functools
import hashlib
import io
import json
import pathlib
import re
import subprocess
import tarfile
import xml.etree.ElementTree as ET


@functools.lru_cache(maxsize=None)
def download(url):
    return subprocess.check_output(['curl', '--fail', '--silent', '--show-error', '--location',
                                    '--retry', '3', '--connect-timeout', '15', '--max-time', '90', url])


def index_content(kind, data, architecture):
    if kind == 'apt':
        # Release dates/signatures change even when the package indexes do not.
        rows = re.findall(r'^ ([a-f0-9]{64})\s+\d+\s+(\S+)$', data.decode(), re.M)
        rows = [(name, digest) for digest, name in rows
                if f'/binary-{architecture}/Packages' in name]
        if not rows:
            raise RuntimeError(f'APT release contains no package indexes for {architecture}')
        return json.dumps(sorted(rows)).encode()
    if kind == 'rpm':
        root = ET.fromstring(data)
        rows = [(item.get('type'), item.find('{*}checksum').text)
                for item in root.findall('{*}data')
                if item.get('type') in ('primary', 'primary_db', 'filelists', 'group', 'group_gz')]
        if not rows:
            raise RuntimeError('RPM repository has no package checksums')
        return json.dumps(sorted(rows)).encode()
    if kind == 'metalink':
        root = ET.fromstring(data)
        hashes = sorted((node.get('type'), node.text) for node in root.findall('.//{*}hash'))
        if not hashes:
            raise RuntimeError('Repository metalink contains no checksums')
        return json.dumps(hashes).encode()
    with tarfile.open(fileobj=io.BytesIO(data), mode='r:*') as archive:
        if kind == 'apk':
            return archive.extractfile('APKINDEX').read()
        # Ignore archive timestamps in pacman's repository database.
        return b'\n'.join(name.encode() + b'\0' + archive.extractfile(name).read()
                          for name in sorted(archive.getnames()) if name.endswith('/desc'))


def xml_repositories(source, filename, variables):
    path = source / filename
    if not path.exists():
        return []
    text = path.read_text()
    # Git snapshots also work on hosts where symlinks are checked out as text.
    if not text.lstrip().startswith('<'):
        text = (path.parent / text.strip()).read_text()
    root = ET.fromstring(text)
    result = []
    for repo in root.findall('repository'):
        url = repo.find('source').get('path')
        for key, value in variables.items():
            url = url.replace('$' + key, value)
        kind = 'metalink' if repo.get('sourcetype') == 'metalink' else 'rpm'
        if kind == 'rpm':
            url = url.rstrip('/') + '/repodata/repomd.xml'
        result.append((kind, url))
    return result


def fingerprint(target, source, repo_root):
    distro, version = target['distribution'], target['version']
    arch = target['platform'].split('/')[1]
    variant = target['platform'].split('/')[2:]
    deb = {'386': 'i386', 'arm64': 'arm64', 'arm': 'armel' if variant == ['v5'] else 'armhf',
           'ppc64le': 'ppc64el'}.get(arch, arch)
    rpm = {'amd64': 'x86_64', 'arm64': 'aarch64', '386': 'i686', 'arm': 'armhfp'}.get(arch, arch)
    # Upstream AlmaLinux's linux/386 compatibility image contains x86_64 packages.
    if distro == 'AlmaLinux' and arch == '386':
        rpm = 'x86_64'
    if distro == 'AlmaLinux' and version == '10' and arch == 'amd64':
        rpm = 'x86_64_v2'
    apk = {'amd64': 'x86_64', 'arm64': 'aarch64', '386': 'x86',
           'arm': 'armhf' if variant == ['v6'] else 'armv7'}.get(arch, arch)
    values = dict(version=version.removeprefix('stream'), deb=deb, rpm=rpm, apk=apk,
                  ubuntu_archive='archive.ubuntu.com/ubuntu' if arch in ('amd64', '386')
                  else 'ports.ubuntu.com/ubuntu-ports',
                  suite=target['branch'].removeprefix('ubuntu/'))
    settings = json.loads((repo_root / distro.lower() / 'repositories.json').read_text())
    urls = [(item['kind'], item['url'].format(**values)) for item in settings
            if int(values['version']) >= item.get('min_version', 0)] if distro in ('RockyLinux',) else [
                (item['kind'], item['url'].format(**values)) for item in settings]
    # The rootfs repositories remain defined by the mirrored upstream descriptions.
    if distro in ('Fedora', 'RockyLinux'):
        variables = dict(releasever=values['version'], basearch=rpm)
        urls += xml_repositories(source, 'repositories/core.xml', variables)
        if distro == 'RockyLinux':
            urls += xml_repositories(source, 'repositories/sig-core.xml', variables)
    if not urls:
        raise RuntimeError(f'No package repositories configured for {distro}')
    result = hashlib.sha256()
    for kind, url in sorted(set(urls)):
        result.update(url.encode() + b'\0' + index_content(kind, download(url), deb) + b'\0')
    return result.hexdigest()
