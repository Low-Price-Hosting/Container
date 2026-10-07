#!/usr/bin/env python3
"""Reset distribution packages or retire superseded, unreferenced build versions."""
import argparse
import hashlib
import json
import pathlib
import re
import subprocess
import sys
from urllib.parse import quote

ORGANIZATION = 'Low-Price-Hosting'
DISTRIBUTIONS = {'ubuntu', 'debian', 'centos', 'alpine', 'fedora', 'almalinux', 'archlinux', 'rockylinux'}
DIGEST = re.compile(r'sha256:[a-f0-9]{64}')
MANIFEST_TYPES = {
    'application/vnd.oci.image.index.v1+json',
    'application/vnd.oci.image.manifest.v1+json',
    'application/vnd.docker.distribution.manifest.list.v2+json',
    'application/vnd.docker.distribution.manifest.v2+json',
}


def github(endpoint, method='GET'):
    command = ['gh', 'api', '--method', method, '-H', 'Accept: application/vnd.github+json',
               '-H', 'X-GitHub-Api-Version: 2022-11-28', endpoint]
    result = subprocess.run(command, text=True, capture_output=True)
    if result.returncode:
        # Do not echo credentials or subprocess arguments from the environment.
        raise RuntimeError(f'GitHub package API failed: {method} {endpoint} (exit {result.returncode})')
    return json.loads(result.stdout) if result.stdout.strip() else None


def pages(endpoint):
    values, page = [], 1
    separator = '&' if '?' in endpoint else '?'
    while True:
        batch = github(f'{endpoint}{separator}per_page=100&page={page}')
        if not isinstance(batch, list):
            raise RuntimeError('Unexpected package list response')
        values.extend(batch)
        if len(batch) < 100:
            return values
        page += 1


def package_endpoint(name):
    return f'orgs/{ORGANIZATION}/packages/container/{quote(name, safe="")}'


def distribution_package(name):
    lower = name.lower()
    return lower in DISTRIBUTIONS or (lower.startswith('container/') and lower[10:] in DISTRIBUTIONS)


def reset():
    endpoint = f'orgs/{ORGANIZATION}/packages?package_type=container'
    packages = [package for package in pages(endpoint) if distribution_package(package['name'])]
    # Capture the inventory before making the explicitly requested deletions.
    inventory = []
    versions_by_package = {}
    for package in packages:
        versions = pages(package_endpoint(package['name']) + '/versions')
        versions_by_package[package['name']] = versions
        repository = package.get('repository') or {}
        inventory.append(dict(id=package['id'], name=package['name'], versions=len(versions),
                              visibility=package.get('visibility', 'unknown'),
                              repository=repository.get('full_name')))
    print(json.dumps(dict(operation='reset', inventory=inventory)), flush=True)
    for package in packages:
        # Delete images while retaining the package's repository link and visibility.
        for version in versions_by_package[package['name']]:
            github(package_endpoint(package['name']) + '/versions/' + str(version['id']), 'DELETE')
        print(json.dumps(dict(cleared_package=package['name'], id=package['id'],
                              deleted_versions=len(versions_by_package[package['name']]))), flush=True)
    remaining = []
    for package in pages(endpoint):
        if distribution_package(package['name']):
            remaining.extend(pages(package_endpoint(package['name']) + '/versions'))
    if remaining:
        raise RuntimeError(f'{len(remaining)} distribution image versions remain after reset')
    print(json.dumps(dict(operation='reset', cleared_packages=len(packages),
                          deleted_versions=sum(item['versions'] for item in inventory), remaining_versions=0)))


def current_release(plan, results, distribution, version, publication):
    if distribution.lower() not in DISTRIBUTIONS:
        raise RuntimeError('Package cleanup is restricted to the configured Linux distributions')
    targets = [target for target in plan['include']
               if target['distribution'] == distribution and target['version'] == version]
    errors = [error for error in plan.get('errors', []) if error['distribution'] == distribution
              and error.get('version', 'sources') in (version, 'sources')]
    statuses = [status for status in publication.get('statuses', [])
                if status[:2] == [distribution, version]]
    if (not targets or errors or len(statuses) != 1 or statuses[0][4] != 'Published'
            or statuses[0][2:4] != [len(targets), len(targets)] or publication.get('failures')):
        raise RuntimeError('Cleanup requires successful publication of every architecture in the release')
    records = {}
    for path in pathlib.Path(results).rglob('image.json'):
        record = json.loads(path.read_text())
        if record['key'] in records:
            raise RuntimeError('Duplicate image approval: ' + record['key'])
        records[record['key']] = record
    repository = f'ghcr.io/{ORGANIZATION.lower()}/{distribution.lower()}'
    protected, tags, images = set(), {version}, []
    platforms = set()
    for target in targets:
        record = records.get(target['key']) or target.get('reused')
        key = '-'.join([distribution.lower(), version, target['platform'].replace('/', '-')])
        if (target.get('error') or not record or record.get('tested') is not True
                or record.get('pushed') is not True or record.get('platform') != target['platform']
                or target['key'] != key or record.get('key') != key
                or record.get('fingerprint') != target.get('fingerprint')
                or not re.fullmatch('[a-f0-9]{64}', target.get('fingerprint', ''))
                or target['platform'] in platforms):
            raise RuntimeError('Cleanup requires matching, pushed runtime-test approvals: ' + target['key'])
        platforms.add(target['platform'])
        reference = record.get('image', '')
        prefix = repository + '@'
        if not reference.startswith(prefix) or not DIGEST.fullmatch(reference[len(prefix):]):
            raise RuntimeError('Cleanup requires an immutable digest from the distribution package')
        protected.add(reference[len(prefix):])
        images.append(reference)
        tags.update(target.get('aliases', []))
        tags.add(f'tested-{key}-sha{target["fingerprint"]}')
        tags.add(f'{version}-{target["platform"].replace("/", "-")}-sha{target["fingerprint"][:16]}')
    index_key = hashlib.sha256('\n'.join(sorted(images)).encode()).hexdigest()[:16]
    tags.add(f'{version}-build{index_key}')
    return repository, protected, tags


def owned_generation_tag(tag, distribution, version):
    release, distro = re.escape(version), re.escape(distribution.lower())
    architecture = r'[a-z0-9]+(?:-[a-z0-9]+)*'
    return bool(re.fullmatch(
        rf'(?:tested-{distro}-{release}-linux-{architecture}-sha[a-f0-9]{{64}}'
        rf'|{release}-linux-{architecture}-sha[a-f0-9]{{16}}'
        rf'|{release}-build[a-f0-9]{{16}})', tag))


def referenced_manifests(repository, roots):
    """Protect each current index and every manifest that its descriptors reference."""
    visited, pending = set(), set(roots)
    while pending:
        digest = pending.pop()
        if digest in visited:
            continue
        if not DIGEST.fullmatch(digest):
            raise RuntimeError('An unsupported digest prevents safe package cleanup')
        result = subprocess.run(['docker', 'buildx', 'imagetools', 'inspect', '--raw',
                                 repository + '@' + digest], text=True, capture_output=True)
        if result.returncode:
            raise RuntimeError('Cannot inspect a protected manifest; package versions were retained')
        manifest = json.loads(result.stdout)
        if manifest.get('schemaVersion') != 2 or manifest.get('mediaType') not in MANIFEST_TYPES:
            raise RuntimeError('An unsupported manifest format prevents safe package cleanup')
        children = manifest.get('manifests', [])
        if not isinstance(children, list):
            raise RuntimeError('Invalid manifest descriptors prevent safe package cleanup')
        descriptors = [*children]
        if manifest.get('subject'):
            descriptors.append(manifest['subject'])
        for child in descriptors:
            child_digest = child.get('digest', '')
            if not DIGEST.fullmatch(child_digest):
                raise RuntimeError('An unsupported child digest prevents safe package cleanup')
            if child_digest not in visited:
                pending.add(child_digest)
        visited.add(digest)
    return visited


def prune(plan, results, distribution, version, publication):
    repository, protected, current_tags = current_release(plan, results, distribution, version, publication)
    endpoint = package_endpoint(distribution.lower())
    versions = pages(endpoint + '/versions')
    candidates, observed_tags = [], set()
    for item in versions:
        digest = item.get('name', '')
        tags = item.get('metadata', {}).get('container', {}).get('tags', [])
        if not isinstance(tags, list) or not all(isinstance(tag, str) for tag in tags):
            raise RuntimeError('Invalid package version metadata prevents safe cleanup')
        observed_tags.update(tags)
        # Untagged manifests are retained. Another OCI index can still reference them.
        if not tags:
            continue
        if not DIGEST.fullmatch(digest):
            print(json.dumps(dict(operation='prune', distribution=distribution, version=version,
                                  skipped='Unsupported package digest; all versions were retained')))
            return
        if any(tag in current_tags or not owned_generation_tag(tag, distribution, version) for tag in tags):
            protected.add(digest)
        else:
            candidates.append(item)
    # The version and aliases are required publication outputs, unlike cache-only tags.
    canonical_tags = {version, *(alias for target in plan['include']
                                if target['distribution'] == distribution and target['version'] == version
                                for alias in target.get('aliases', []))}
    if not canonical_tags.issubset(observed_tags):
        raise RuntimeError('Published version/alias tags are missing; package versions were retained')
    if not candidates:
        print(json.dumps(dict(operation='prune', package=distribution.lower(), version=version,
                              deleted_versions=0, retained_versions=len(versions))))
        return
    try:
        protected = referenced_manifests(repository, protected)
    except (RuntimeError, json.JSONDecodeError) as error:
        print(json.dumps(dict(operation='prune', distribution=distribution, version=version,
                              skipped=str(error), deleted_versions=0)))
        return
    obsolete = [item for item in candidates if item['name'] not in protected]
    for item in obsolete:
        github(endpoint + '/versions/' + str(item['id']), 'DELETE')
        print(json.dumps(dict(deleted_version=item['id'], package=distribution.lower(),
                              digest=item['name'], tags=item['metadata']['container']['tags'])), flush=True)
    print(json.dumps(dict(operation='prune', package=distribution.lower(), version=version,
                          deleted_versions=len(obsolete), retained_versions=len(versions) - len(obsolete))))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    operations = parser.add_subparsers(dest='operation', required=True)
    operations.add_parser('reset', help='Delete every distribution image version, preserving package settings')
    cleanup = operations.add_parser('prune', help='Retire unreferenced generations after a successful release publication')
    cleanup.add_argument('plan', type=pathlib.Path)
    cleanup.add_argument('results', type=pathlib.Path)
    cleanup.add_argument('--distribution', required=True)
    cleanup.add_argument('--version', required=True)
    cleanup.add_argument('--publication', type=pathlib.Path, required=True)
    args = parser.parse_args()
    if args.operation == 'reset':
        reset()
    else:
        prune(json.loads(args.plan.read_text()), args.results, args.distribution, args.version,
              json.loads(args.publication.read_text()))


if __name__ == '__main__':
    try:
        main()
    except (RuntimeError, ValueError, KeyError) as error:
        print(str(error), file=sys.stderr)
        sys.exit(1)
