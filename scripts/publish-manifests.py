#!/usr/bin/env python3
"""Publish aliases only after every architecture passed its runtime test."""
import collections
import argparse
import hashlib
import json
import os
import pathlib
import subprocess
import sys

def scoped_plan(plan, distribution, version):
    return dict(include=[t for t in plan['include'] if t['distribution'] == distribution and t['version'] == version],
                errors=[e for e in plan.get('errors', []) if e['distribution'] == distribution
                        and e.get('version', 'sources') == version])


def publish(plan, directory, validate_only=False):
    records = {}
    for path in pathlib.Path(directory).rglob('image.json'):
        item = json.loads(path.read_text())
        if item['key'] in records:
            raise RuntimeError(f"Duplicate build result: {item['key']}")
        records[item['key']] = item
    groups = collections.defaultdict(list)
    for target in plan['include']:
        groups[(target['distribution'], target['version'])].append(target)
    statuses = []
    failures = list(plan.get('errors', []))
    for (distribution, version), targets in groups.items():
        images, missing = [], []
        for target in targets:
            item = records.get(target['key']) or target.get('reused')
            if (not item or not item.get('tested') or (not validate_only and not item.get('pushed'))
                    or item['platform'] != target['platform']
                    or item.get('fingerprint') != target.get('fingerprint') or target.get('error')):
                missing.append(target['platform'])
            else:
                images.append(item['image'])
        if missing:
            failures.append(dict(distribution=distribution, version=version, error='Untested/missing: ' + ', '.join(missing)))
            statuses.append((distribution, version, len(images), len(targets), 'Skipped: incomplete tests'))
            continue
        if validate_only:
            statuses.append((distribution, version, len(images), len(targets), 'Tests passed; publication disabled'))
            continue
        repository = 'ghcr.io/low-price-hosting/' + distribution.lower()
        images.sort()
        digest = hashlib.sha256('\n'.join(images).encode()).hexdigest()[:16]
        tags = sorted({version, *(alias for target in targets for alias in target['aliases'])})
        try:
            args = ['docker', 'buildx', 'imagetools', 'create',
                    '--annotation', 'index:io.low-price-hosting.release.inputs=' + digest,
                    '--tag', f'{repository}:{version}-build{digest}']
            for tag in tags:
                args += ['--tag', repository + ':' + tag]
            subprocess.run([*args, *images], check=True)
            statuses.append((distribution, version, len(images), len(targets), 'Published'))
        except subprocess.CalledProcessError as error:
            failures.append(dict(distribution=distribution, version=version, error=str(error)))
            statuses.append((distribution, version, len(images), len(targets), 'Publish failed'))
    summary = os.environ.get('GITHUB_STEP_SUMMARY')
    if summary:
        with open(summary, 'a') as stream:
            stream.write('## Release publication\n\n| Distribution | Version | Tested architectures | Result |\n|---|---|---|---|\n')
            for distribution, version, passed, expected, status in statuses:
                stream.write(f'| {distribution} | {version} | {passed}/{expected} | {status} |\n')
            for failure in failures:
                stream.write(f"\n**{failure['distribution']} {failure.get('version', '')}:** {failure['error']}\n")
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
