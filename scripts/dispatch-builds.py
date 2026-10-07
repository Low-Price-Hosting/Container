#!/usr/bin/env python3
"""Start the same release workflow for every dynamically discovered release."""
import argparse
import json
import os
import pathlib
import sys
import urllib.error
import urllib.request


def dispatch(plan, verify_only=False):
    repository = os.environ['GITHUB_REPOSITORY']
    url = f'{os.environ.get("GITHUB_API_URL", "https://api.github.com")}/repos/{repository}/actions/workflows/build-release.yml/dispatches'
    headers = {'Authorization': 'Bearer ' + os.environ['GH_TOKEN'], 'Accept': 'application/vnd.github+json',
               'Content-Type': 'application/json', 'X-GitHub-Api-Version': '2026-03-10'}
    results = []
    failures = [e for e in plan.get('errors', []) if 'version' not in e]
    for release in plan['releases']['include']:
        if release['version'] == 'sources':
            continue
        inputs = {
            'distribution': release['distribution'], 'version': release['version'],
            'release-key': release['key'], 'targets': json.dumps(release['targets'], separators=(',', ':')),
            'has-changes': str(release['has_changes']).lower(), 'has-errors': str(release['has_errors']).lower(),
            'verify-only': str(verify_only).lower(), 'plan-run-id': os.environ['GITHUB_RUN_ID'],
            'source-ref': os.environ['GITHUB_SHA'],
        }
        body = json.dumps({'ref': os.environ.get('GITHUB_REF_NAME', 'main'), 'inputs': inputs}).encode()
        request = urllib.request.Request(url, data=body, headers=headers, method='POST')
        try:
            with urllib.request.urlopen(request, timeout=30) as response:
                data = response.read()
                run = json.loads(data) if data else {}
            results.append(dict(distribution=release['distribution'], version=release['version'],
                                architectures=len(release['targets']), **run))
        except (urllib.error.HTTPError, urllib.error.URLError, TimeoutError) as error:
            failures.append(dict(distribution=release['distribution'], version=release['version'], error=str(error)))
    summary = os.environ.get('GITHUB_STEP_SUMMARY')
    if summary:
        with open(summary, 'a') as stream:
            stream.write('## Release workflows\n\n| Release | Architectures to build | Run |\n|---|---|---|\n')
            for result in results:
                link = result.get('html_url', f'https://github.com/{repository}/actions/workflows/build-release.yml')
                stream.write(f"| {result['distribution']} {result['version']} | {result['architectures']} | [Open run]({link}) |\n")
            if not results and not failures:
                stream.write('\nAll tested images and release tags are current. No build runners started.\n')
            for failure in failures:
                stream.write(f"\n**{failure['distribution']} {failure.get('version', '')}:** {failure['error']}\n")
    print(json.dumps(results))
    for failure in failures:
        print(failure, file=sys.stderr)
    return 1 if failures else 0


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('plan', type=pathlib.Path)
    parser.add_argument('--verify-only', action='store_true')
    args = parser.parse_args()
    sys.exit(dispatch(json.loads(args.plan.read_text()), args.verify_only))
