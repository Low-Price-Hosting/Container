#!/usr/bin/env python3
"""Give every discovered release its own job in the Actions graph."""
import concurrent.futures
import importlib.util
import json
import pathlib
import re
import sys
import tempfile

ROOT = pathlib.Path(__file__).resolve().parent.parent
spec = importlib.util.spec_from_file_location('discovery', ROOT / 'scripts/discover-builds.py')
discovery = importlib.util.module_from_spec(spec)
spec.loader.exec_module(discovery)
CATALOG = ROOT / 'scripts/release-jobs.json'
WORKFLOW = ROOT / '.github/workflows/build-base-images.yml'


def render(catalog):
    workflow = (ROOT / 'scripts/build-workflow.yml.in').read_text()
    identifiers = set()
    for distribution in discovery.DISTRIBUTIONS:
        versions = set(catalog.get(distribution, []))
        order = lambda v: tuple(int(p) if p.isdecimal() else p for p in re.split(r'(\d+)', v))
        for version in sorted(versions, key=order, reverse=True):
            if not re.fullmatch(r'[A-Za-z0-9][A-Za-z0-9_.-]{0,32}', version):
                raise ValueError(f'Invalid release version: {distribution}/{version}')
            identifier = discovery.release_job_id(distribution, version)
            if identifier in identifiers:
                raise ValueError(f'Conflicting release job: {identifier}')
            identifiers.add(identifier)
            release = 'fromJSON(needs.discover.outputs.releases).' + identifier
            expression = lambda value: '${{ ' + value + ' }}'
            workflow += '\n' + '\n'.join([
                '  ' + identifier + ':',
                '    name: ' + json.dumps('Build: ' + distribution + ' ' + version),
                '    needs: discover',
                '    if: ' + expression(release + ' != null'),
                '    uses: ./.github/workflows/build-release.yml',
                '    with:',
                '      distribution: ' + json.dumps(distribution),
                '      version: ' + json.dumps(version),
                '      release-key: ' + json.dumps(distribution.lower() + '-' + version),
                '      targets: ' + expression('toJSON(' + release + '.targets)'),
                '      has-changes: ' + expression(release + '.has_changes'),
                '      has-errors: ' + expression(release + '.has_errors'),
                '      verify-only: ${{ inputs.verify_only || false }}',
                '    secrets:',
                '      GH_TOKEN_CLASSIC: ${{ secrets.GH_TOKEN_CLASSIC }}',
                '',
            ])
    if not identifiers:
        raise ValueError('No release jobs discovered')
    return workflow


def update():
    catalog = json.loads(CATALOG.read_text()) if CATALOG.exists() else {}
    with tempfile.TemporaryDirectory(prefix='release-job-catalog-') as directory:
        def collect(distribution):
            _, releases = discovery.source_catalog(distribution, pathlib.Path(directory) / distribution)
            return sorted({r['version'] for r in releases})
        with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:
            futures = {d: pool.submit(collect, d) for d in discovery.DISTRIBUTIONS}
            for distribution, future in futures.items():
                try:
                    catalog[distribution] = future.result()
                except Exception as error:
                    print(f'{distribution}: keeping previous release jobs: {error}', file=sys.stderr)
                    if distribution not in catalog:
                        raise
    workflow = render(catalog)
    CATALOG.write_text(json.dumps(catalog, indent=2) + '\n', newline='\n')
    WORKFLOW.write_text(workflow, newline='\n')


if __name__ == '__main__':
    update()
