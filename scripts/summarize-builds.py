#!/usr/bin/env python3
"""Collect stage results into a single summary grouped by architecture."""
import argparse
import collections
import json
import os
import pathlib
import sys


def record(path):
    target = json.loads(os.environ['BUILD_TARGET'])
    stages = {name: os.environ[name.upper() + '_RESULT'] or 'skipped'
              for name in ('build', 'test', 'push') if name.upper() + '_RESULT' in os.environ}
    if 'CACHE_HIT' in os.environ:
        stages['cache'] = os.environ['CACHE_HIT'] == 'true'
    path.write_text(json.dumps(dict(key=target['key'], **stages)))


def cell(value):
    return str(value).replace('linux/', '').replace('|', '\\|').replace('\n', ' ')


def report(plan, directory):
    records = {}
    for path in directory.rglob('status.json'):
        item = json.loads(path.read_text())
        result = records.setdefault(item['key'], {})
        stages = {name: value for name, value in item.items() if name != 'key'}
        if result.keys() & stages.keys():
            raise RuntimeError(f"Duplicate stage result: {item['key']}")
        result.update(stages)
    publications = {}
    failures = list(plan.get('errors', []))
    for path in directory.rglob('publication.json'):
        result = json.loads(path.read_text())
        failures += result['failures']
        for distribution, version, passed, expected, status in result['statuses']:
            publications[(distribution, version)] = (f'{passed}/{expected}', status)
    groups = collections.defaultdict(list)
    for target in plan['include']:
        groups[target['platform'].removeprefix('linux/')].append(target)
    lines = ['# Build results', '']
    if plan.get('verify_only'):
        lines += ['Verification run: images were built and tested; pushing was disabled.', '']
    for architecture, targets in sorted(groups.items()):
        lines += [f'## {cell(architecture)}', '',
                  '| Distribution | Version | Build | Test | Push | Package cache |',
                  '|---|---|---|---|---|---|']
        for target in sorted(targets, key=lambda t: (t['distribution'], t['version'])):
            if target.get('error'):
                values = ('Source error', 'skipped', 'skipped', '—')
                failures.append(dict(distribution=target['distribution'], version=target['version'],
                                     error=target['error']))
            elif target.get('reused'):
                values = ('Reused', 'Previously passed', 'Current', '—')
            elif target['key'] in records:
                result = records[target['key']]
                values = (*(result.get(stage, 'skipped') for stage in ('build', 'test', 'push')),
                          'Restored' if result.get('cache') else 'Miss')
                if (result.get('build') != 'success' or result.get('test') != 'success'
                        or (not plan.get('verify_only') and result.get('push') != 'success')):
                    failures.append(dict(distribution=target['distribution'], version=target['version'],
                                         error='Incomplete build/test/push: ' + target['platform']))
            else:
                values = ('No result', 'No result', 'No result', '—')
                failures.append(dict(distribution=target['distribution'], version=target['version'],
                                     error='Missing stage result: ' + target['platform']))
            lines.append('| ' + ' | '.join(cell(v) for v in (target['distribution'], target['version'], *values)) + ' |')
        lines.append('')
    lines += ['## Release tags', '', '| Distribution | Version | Tested architectures | Result |', '|---|---|---|---|']
    scheduled = {(r['distribution'], r['version']) for r in plan['releases']['include'] if r['version'] != 'sources'}
    all_releases = {(t['distribution'], t['version']) for t in plan['include']} | scheduled
    for distribution, version in sorted(all_releases):
        if (distribution, version) in publications:
            tested, status = publications[(distribution, version)]
        elif (distribution, version) not in scheduled:
            tested = str(sum(t['distribution'] == distribution and t['version'] == version for t in plan['include']))
            status = 'Current; no rebuild needed'
        else:
            tested, status = '—', 'No publication result'
            failures.append(dict(distribution=distribution, version=version, error=status))
        lines.append('| ' + ' | '.join(cell(v) for v in (distribution, version, tested, status)) + ' |')
    lines.append('')
    if failures:
        lines += ['## Errors', '']
        for message in sorted({f"{e['distribution']} {e.get('version', '')}: {e['error']}" for e in failures}):
            lines.append('- ' + cell(message))
        lines.append('')
    text = '\n'.join(lines)
    pathlib.Path(os.environ.get('RUNNER_TEMP', '.')).joinpath('results-summary.md').write_text(text, encoding='utf-8')
    if os.environ.get('GITHUB_STEP_SUMMARY'):
        with open(os.environ['GITHUB_STEP_SUMMARY'], 'a', encoding='utf-8') as stream:
            stream.write(text)
    print(text)
    return int(bool(failures))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    commands = parser.add_subparsers(dest='mode', required=True)
    commands.add_parser('record').add_argument('path', type=pathlib.Path)
    reporter = commands.add_parser('report')
    reporter.add_argument('plan', type=pathlib.Path)
    reporter.add_argument('results', type=pathlib.Path)
    args = parser.parse_args()
    if args.mode == 'record':
        record(args.path)
    else:
        sys.exit(report(json.loads(args.plan.read_text()), args.results))
