#!/usr/bin/env python3
"""Push tested architectures one at a time, then publish their release aliases."""
import argparse
import importlib.util
import json
import os
import pathlib
import re
import subprocess
import sys
import tempfile


ROOT = pathlib.Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location('publication', ROOT / 'publish-manifests.py')
publication = importlib.util.module_from_spec(spec)
spec.loader.exec_module(publication)


def save_failure(distribution, version, error):
    destination = os.environ.get('PUBLICATION_RESULT')
    if destination:
        pathlib.Path(destination).write_text(json.dumps(dict(statuses=[], failures=[
            dict(distribution=distribution, version=version, error=str(error))])), encoding='utf-8')
    print(str(error), file=sys.stderr)


def publish_release(plan, results, distribution, version, validate_only=False):
    plan = publication.scoped_plan(plan, distribution, version)
    if not plan['include'] and not plan['errors']:
        save_failure(distribution, version, 'Release is missing from the discovered build plan')
        return 1
    try:
        # No image is pushed until the complete architecture set passed its tests.
        validation = publication.publish(plan, results, validate_only=True)
    except Exception as error:
        save_failure(distribution, version, error)
        return 1
    if validation or validate_only:
        return validation

    runner_temp = pathlib.Path(os.environ['RUNNER_TEMP'])
    records = {json.loads(path.read_text())['key']: path for path in results.rglob('image.json')}
    failed = False
    try:
        for target in plan['include']:
            if target.get('reused'):
                continue
            key = target['key']
            status = dict(key=key, push='failure')
            reference = None
            try:
                if not re.fullmatch(r'[A-Za-z0-9][A-Za-z0-9._-]*', key):
                    raise ValueError(f'Invalid image artifact key: {key}')
                tested_path = records[key]
                tested = json.loads(tested_path.read_text())
                if tested.get('pushed') is not False:
                    raise ValueError(f'Image must be tested and awaiting publication: {key}')
                reference = tested['image']
                with tempfile.TemporaryDirectory(prefix='release-image-', dir=runner_temp) as directory:
                    artifact = pathlib.Path(directory)
                    subprocess.run(['gh', 'run', 'download', os.environ['GITHUB_RUN_ID'],
                                    '--repo', os.environ['GITHUB_REPOSITORY'], '--name', 'built-' + key,
                                    '--dir', str(artifact)], check=True)
                    built = json.loads((artifact / 'image.json').read_text())
                    for field in ('key', 'platform', 'image', 'fingerprint', 'archive_sha256'):
                        if not tested.get(field) or built.get(field) != tested[field]:
                            raise ValueError(f'Built and tested image differ ({field}): {key}')
                    if built.get('tested') is not False or built.get('pushed') is not False:
                        raise ValueError(f'Unexpected state in built image artifact: {key}')
                    subprocess.run(['bash', str(ROOT / 'image-artifact.sh'), 'restore', str(artifact)], check=True)
                    (runner_temp / 'image.json').write_text(json.dumps(tested), encoding='utf-8')
                    subprocess.run(['bash', str(ROOT / 'push-images.sh')], check=True)
                    pushed = json.loads((runner_temp / 'image.json').read_text())
                    if (pushed.get('tested') is not True or pushed.get('pushed') is not True
                            or not re.search(r'@sha256:[a-f0-9]{64}$', pushed.get('image', ''))
                            or any(pushed.get(field) != tested[field]
                                   for field in ('key', 'platform', 'fingerprint', 'archive_sha256'))):
                        raise ValueError(f'Incomplete pushed image result: {key}')
                    tested_path.write_text(json.dumps(pushed), encoding='utf-8')
                    status['push'] = 'success'
            except Exception as error:
                failed = True
                print(f'{key}: {error}', file=sys.stderr)
            finally:
                if reference:
                    # The push helper removes successful images; this also covers a failed push/load.
                    subprocess.run(['docker', 'image', 'rm', '--force', reference], check=False,
                                   stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                if re.fullmatch(r'[A-Za-z0-9][A-Za-z0-9._-]*', key):
                    destination = runner_temp / 'push-status' / key / 'status.json'
                    destination.parent.mkdir(parents=True, exist_ok=True)
                    destination.write_text(json.dumps(status), encoding='utf-8')
            if failed:
                break
    finally:
        # Missing/failed pushes leave records unpushed, preventing partial release aliases.
        try:
            published = publication.publish(plan, results, validate_only=False)
        except Exception as error:
            save_failure(distribution, version, error)
            published = 1
    return int(failed or bool(published))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('plan', type=pathlib.Path)
    parser.add_argument('results', type=pathlib.Path)
    parser.add_argument('--distribution', required=True)
    parser.add_argument('--version', required=True)
    parser.add_argument('--validate-only', action='store_true')
    args = parser.parse_args()
    sys.exit(publish_release(json.loads(args.plan.read_text()), args.results,
                             args.distribution, args.version, args.validate_only))
