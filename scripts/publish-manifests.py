#!/usr/bin/env python3
"""Publish one OCI index containing every tested architecture of a release."""
import argparse
import base64
import collections
import hashlib
import json
import os
import pathlib
import re
import sys
import time
import urllib.error
import urllib.parse
import urllib.request


INDEX_TYPE = 'application/vnd.oci.image.index.v1+json'
IMAGE_TYPES = {'application/vnd.oci.image.manifest.v1+json',
               'application/vnd.docker.distribution.manifest.v2+json'}
TAG_PATTERN = r'[A-Za-z0-9_][A-Za-z0-9._-]{0,127}'


def scoped_plan(plan, distribution, version):
    return dict(include=[t for t in plan['include'] if t['distribution'] == distribution and t['version'] == version],
                errors=[e for e in plan.get('errors', []) if e['distribution'] == distribution
                        and e.get('version', 'sources') == version])


def platform_descriptor(platform):
    parts = platform.split('/')
    if len(parts) not in (2, 3) or parts[0] != 'linux' or parts[1] == 'unknown':
        raise ValueError(f'Invalid runtime platform: {platform}')
    return dict(os=parts[0], architecture=parts[1], **({'variant': parts[2]} if len(parts) == 3 else {}))


def release_index(distribution, version, targets, records):
    repository = 'ghcr.io/low-price-hosting/' + distribution.lower()
    descriptors, images, os_versions = [], [], set()
    for target in sorted(targets, key=lambda item: item['platform']):
        item = records[target['key']]
        descriptor = item.get('descriptor', {})
        digest = descriptor.get('digest', '')
        annotations = descriptor.get('annotations', {})
        if (not re.fullmatch(r'sha256:[a-f0-9]{64}', digest)
                or item['image'] != repository + '@' + digest
                or descriptor.get('mediaType') not in IMAGE_TYPES
                or not isinstance(descriptor.get('size'), int) or descriptor['size'] <= 0
                or descriptor.get('platform') != platform_descriptor(target['platform'])
                or not re.fullmatch(r'[a-f0-9]{64}', target['fingerprint'])
                or annotations.get('io.low-price-hosting.build.inputs') != target['fingerprint']
                or annotations.get('io.low-price-hosting.os.version') != item.get('os_version')
                or annotations.get('io.low-price-hosting.tested') != 'true'):
            raise ValueError(f'Invalid tested image descriptor: {target["key"]}')
        descriptors.append(descriptor)
        images.append(item['image'])
        os_versions.add(item.get('os_version'))
    if len({target['platform'] for target in targets}) != len(targets):
        raise ValueError('Duplicate release architecture')
    tags = {version, *(alias for target in targets for alias in target['aliases'])}
    actual_version = next(iter(os_versions)) if len(os_versions) == 1 else None
    if actual_version and re.fullmatch(TAG_PATTERN, actual_version):
        tags.add(actual_version)
    if any(not re.fullmatch(TAG_PATTERN, tag) for tag in tags):
        raise ValueError('Invalid release tag')
    source = 'https://github.com/Low-Price-Hosting/' + distribution
    architectures = ', '.join(target['platform'].removeprefix('linux/') for target in sorted(targets, key=lambda item: item['platform']))
    annotations = {
        'org.opencontainers.image.source': source,
        'org.opencontainers.image.url': source,
        'org.opencontainers.image.title': distribution + ' ' + version,
        'org.opencontainers.image.description': f'{distribution} {actual_version or version} base image. Architectures: {architectures}. Built from {source}.',
        'org.opencontainers.image.version': version,
        'org.opencontainers.image.vendor': 'Low-Price-Hosting',
        'io.low-price-hosting.build.source': 'https://github.com/Low-Price-Hosting/Container',
        'io.low-price-hosting.release.schema': '2',
        'io.low-price-hosting.release.inputs': hashlib.sha256('\n'.join(sorted(images)).encode()).hexdigest(),
    }
    if actual_version:
        annotations['io.low-price-hosting.os.version'] = actual_version
    index = dict(schemaVersion=2, mediaType=INDEX_TYPE, manifests=descriptors, annotations=annotations)
    # Publish latest last so the default installation example points at a release.
    ordered_tags = [version, *sorted(tags - {version, 'latest'})]
    if 'latest' in tags and version != 'latest':
        ordered_tags.append('latest')
    return repository, ordered_tags, index


def registry_request(request):
    for attempt in range(3):
        try:
            with urllib.request.urlopen(request, timeout=60) as response:
                return response.read(), response.headers
        except urllib.error.HTTPError as error:
            if error.code not in (408, 429, 500, 502, 503, 504) or attempt == 2:
                raise RuntimeError(f'GHCR request failed (HTTP {error.code}): {request.get_method()} {request.full_url}') from None
        except urllib.error.URLError:
            if attempt == 2:
                raise RuntimeError(f'GHCR connection failed: {request.get_method()} {request.full_url}') from None
        time.sleep(5 * (attempt + 1))


def publish_index(repository, tags, index):
    # The tested child manifests are already present in this repository by digest.
    # PUT the OCI index directly to preserve descriptor annotations and variants.
    name = repository.removeprefix('ghcr.io/')
    credentials = base64.b64encode((os.environ['GITHUB_ACTOR'] + ':' + os.environ['GH_TOKEN']).encode()).decode()
    query = urllib.parse.urlencode(dict(service='ghcr.io', scope=f'repository:{name}:pull,push'))
    token_body, _ = registry_request(urllib.request.Request('https://ghcr.io/token?' + query,
                                    headers={'Authorization': 'Basic ' + credentials}))
    bearer = json.loads(token_body).get('token') or json.loads(token_body)['access_token']
    body = json.dumps(index, separators=(',', ':'), sort_keys=True).encode()
    expected = 'sha256:' + hashlib.sha256(body).hexdigest()
    for tag in tags:
        url = 'https://ghcr.io/v2/' + name + '/manifests/' + tag
        headers = {'Authorization': 'Bearer ' + bearer, 'Content-Type': INDEX_TYPE}
        _, response_headers = registry_request(urllib.request.Request(url, data=body, headers=headers, method='PUT'))
        if response_headers.get('Docker-Content-Digest', expected) != expected:
            raise RuntimeError(f'GHCR returned a different index digest: {repository}:{tag}')
        published, _ = registry_request(urllib.request.Request(url,
                            headers={'Authorization': 'Bearer ' + bearer, 'Accept': INDEX_TYPE}))
        if hashlib.sha256(published).hexdigest() != expected.removeprefix('sha256:'):
            raise RuntimeError(f'Published release verification failed: {repository}:{tag}')
        print(f'Published {repository}:{tag} ({len(index["manifests"])} architectures)')


def publish(plan, directory, validate_only=False):
    records = {}
    for path in pathlib.Path(directory).rglob('image.json'):
        item = json.loads(path.read_text())
        if item['key'] in records:
            raise RuntimeError(f'Duplicate build result: {item["key"]}')
        records[item['key']] = item
    groups = collections.defaultdict(list)
    for target in plan['include']:
        groups[(target['distribution'], target['version'])].append(target)
    statuses = []
    failures = list(plan.get('errors', []))
    for (distribution, version), targets in groups.items():
        approved, missing = {}, []
        for target in targets:
            item = records.get(target['key']) or target.get('reused')
            if (not item or item.get('tested') is not True or (not validate_only and item.get('pushed') is not True)
                    or item['platform'] != target['platform']
                    or item.get('fingerprint') != target.get('fingerprint') or target.get('error')):
                missing.append(target['platform'])
            else:
                approved[target['key']] = item
        if missing:
            failures.append(dict(distribution=distribution, version=version, error='Untested/missing: ' + ', '.join(missing)))
            statuses.append((distribution, version, len(approved), len(targets), 'Skipped: incomplete tests'))
            continue
        if validate_only:
            statuses.append((distribution, version, len(approved), len(targets), 'Tests passed; publication disabled'))
            continue
        try:
            publish_index(*release_index(distribution, version, targets, approved))
            statuses.append((distribution, version, len(approved), len(targets), 'Published'))
        except Exception as error:
            failures.append(dict(distribution=distribution, version=version, error=str(error)))
            statuses.append((distribution, version, len(approved), len(targets), 'Publish failed'))
    result = os.environ.get('PUBLICATION_RESULT')
    if result:
        pathlib.Path(result).write_text(json.dumps(dict(statuses=statuses, failures=failures)))
    print(json.dumps(statuses))
    for failure in failures:
        print(failure, file=sys.stderr)
    return 1 if failures else 0


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('plan', type=pathlib.Path)
    parser.add_argument('results')
    parser.add_argument('--distribution', required=True)
    parser.add_argument('--version', required=True)
    parser.add_argument('--validate-only', action='store_true')
    args = parser.parse_args()
    plan = scoped_plan(json.loads(args.plan.read_text()), args.distribution, args.version)
    if not plan['include'] and not plan['errors']:
        raise RuntimeError('Release is missing from the discovered build plan')
    sys.exit(publish(plan, args.results, args.validate_only))
