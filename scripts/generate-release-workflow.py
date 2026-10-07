#!/usr/bin/env python3
"""Generate distinct graph groups from the organization's release catalogs."""
import importlib.util
import json
import pathlib
import collections
import sys
import tempfile

ROOT = pathlib.Path(__file__).resolve().parent.parent
WORKFLOW = ROOT / '.github/workflows/build-base-images.yml'
TEMPLATE = ROOT / 'scripts/build-workflow.yml.in'
spec = importlib.util.spec_from_file_location('discovery', ROOT / 'scripts/discover-builds.py')
discovery = importlib.util.module_from_spec(spec)
spec.loader.exec_module(discovery)
MARKER = '# release-group-capacity: '


def previous_catalog(text):
    for line in text.splitlines():
        if line.startswith(MARKER):
            counts = json.loads(line[len(MARKER):])
            return [dict(distribution=d, version=f'capacity-{i}') for d, count in counts.items()
                    for i in range(count)]
    # Read the previous generated format during the migration.
    legacy = '  # release-group: '
    return [json.loads(line[len(legacy):]) for line in text.splitlines() if line.startswith(legacy)]


def collect_catalog(previous):
    result = []
    with tempfile.TemporaryDirectory(prefix='container-release-groups-') as temp:
        for distribution in discovery.DISTRIBUTIONS:
            try:
                _, releases = discovery.source_catalog(distribution, pathlib.Path(temp) / distribution)
                result += [dict(distribution=distribution, version=r['version']) for r in releases]
            except Exception as error:
                fallback = [r for r in previous if r['distribution'] == distribution]
                if not fallback:
                    raise RuntimeError(f'Cannot create release groups for {distribution}: {error}') from error
                print(f'{distribution}: keep existing groups; catalog unavailable: {error}', file=sys.stderr)
                result += fallback
    return result


def render(catalog, template):
    catalog = [dict(distribution=d, version=v) for d, v in sorted({(r['distribution'], r['version']) for r in catalog})]
    counts = dict(sorted(collections.Counter(r['distribution'] for r in catalog).items()))
    jobs, identifiers = [], []
    for index in range(1, len(catalog) + 1):
        identifier = f'Build_Group_{index:02d}'
        identifiers.append(identifier)
        detail = f"fromJSON(needs.discover.outputs.groups || '{{}}')['{index}']"
        jobs.append(f'''  {identifier}:
    name: ${{{{ {detail}.name || 'Group {index} (idle)' }}}}
    needs: discover
    if: contains(fromJSON(needs.discover.outputs.active-groups || '[]'), '{index}')
    uses: ./.github/workflows/build-release.yml
    with:
      distribution: ${{{{ {detail}.distribution }}}}
      version: ${{{{ {detail}.version }}}}
      release-key: ${{{{ {detail}.key }}}}
      targets: ${{{{ toJSON({detail}.targets) }}}}
      has-changes: ${{{{ {detail}.has_changes }}}}
      verify-only: ${{{{ inputs.verify_only || false }}}}
    secrets:
      GH_TOKEN_CLASSIC: ${{{{ secrets.GH_TOKEN_CLASSIC }}}}
''')
    if not identifiers:
        raise ValueError('No release groups discovered')
    return template.replace('__RELEASE_JOBS__', MARKER + json.dumps(counts, separators=(',', ':'))
                            + '\n' + '\n'.join(jobs)).replace('__RELEASE_NEEDS__', ', '.join(identifiers))


if __name__ == '__main__':
    old = WORKFLOW.read_text(encoding='utf-8') if WORKFLOW.exists() else ''
    catalog = collect_catalog(previous_catalog(old))
    new = render(catalog, TEMPLATE.read_text(encoding='utf-8'))
    if new != old:
        WORKFLOW.write_text(new, encoding='utf-8', newline='\n')
    print(json.dumps(dict(releases=len({(r['distribution'], r['version']) for r in catalog}), changed=new != old)))
