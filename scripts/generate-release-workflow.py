#!/usr/bin/env python3
"""Generate distinct graph groups from the organization's release catalogs."""
import importlib.util
import json
import pathlib
import re
import sys
import tempfile

ROOT = pathlib.Path(__file__).resolve().parent.parent
WORKFLOW = ROOT / '.github/workflows/build-base-images.yml'
TEMPLATE = ROOT / 'scripts/build-workflow.yml.in'
spec = importlib.util.spec_from_file_location('discovery', ROOT / 'scripts/discover-builds.py')
discovery = importlib.util.module_from_spec(spec)
spec.loader.exec_module(discovery)
MARKER = '  # release-group: '


def job_id(distribution, version):
    if distribution not in discovery.DISTRIBUTIONS or not re.fullmatch(r'[A-Za-z0-9._-]+', version):
        raise ValueError(f'Invalid release: {distribution} {version}')
    return 'Build_' + distribution + '_' + re.sub(r'[^A-Za-z0-9_]', '_', version)


def previous_catalog(text):
    return [json.loads(line[len(MARKER):]) for line in text.splitlines() if line.startswith(MARKER)]


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
    jobs, identifiers = [], []
    for release in catalog:
        distribution, version = release['distribution'], release['version']
        identifier = job_id(distribution, version)
        if identifier in identifiers:
            raise ValueError(f'Colliding release job: {identifier}')
        identifiers.append(identifier)
        key = distribution.lower() + '-' + version
        detail = f"fromJSON(needs.discover.outputs.groups)['{key}']"
        jobs.append(MARKER + json.dumps(release, separators=(',', ':')) + '\n' + f'''  {identifier}:
    name: {distribution} {version}
    needs: discover
    if: contains(fromJSON(needs.discover.outputs.active-groups), '{key}')
    uses: ./.github/workflows/build-release.yml
    with:
      distribution: {json.dumps(distribution)}
      version: {json.dumps(version)}
      release-key: {json.dumps(key)}
      targets: ${{{{ toJSON({detail}.targets) }}}}
      has-changes: ${{{{ {detail}.has_changes }}}}
      verify-only: ${{{{ inputs.verify_only || false }}}}
    secrets:
      GH_TOKEN_CLASSIC: ${{{{ secrets.GH_TOKEN_CLASSIC }}}}
''')
    if not identifiers:
        raise ValueError('No release groups discovered')
    return template.replace('__RELEASE_JOBS__', '\n'.join(jobs)).replace('__RELEASE_NEEDS__', ', '.join(identifiers))


if __name__ == '__main__':
    old = WORKFLOW.read_text(encoding='utf-8') if WORKFLOW.exists() else ''
    catalog = collect_catalog(previous_catalog(old))
    new = render(catalog, TEMPLATE.read_text(encoding='utf-8'))
    if new != old:
        WORKFLOW.write_text(new, encoding='utf-8', newline='\n')
    print(json.dumps(dict(releases=len({(r['distribution'], r['version']) for r in catalog}), changed=new != old)))
