#!/usr/bin/env python3
"""Publish aliases only after every architecture passed its runtime test."""
import collections
import hashlib
import json
import pathlib
import subprocess
import sys

plan = json.loads(pathlib.Path(sys.argv[1]).read_text())['include']
records = {}
for path in pathlib.Path(sys.argv[2]).rglob('image.json'):
    item = json.loads(path.read_text())
    if item['key'] in records:
        raise RuntimeError(f"Duplicate build result: {item['key']}")
    records[item['key']] = item
groups = collections.defaultdict(list)
for target in plan:
    item = records[target['key']]
    if item['platform'] != target['platform']:
        raise RuntimeError('Architecture differs from the build plan')
    groups[(target['distribution'], target['version'])].append((target, item))
for (distribution, version), items in groups.items():
    images = sorted(item['image'] for _, item in items)
    repository = 'ghcr.io/low-price-hosting/' + distribution.lower()
    digest = hashlib.sha256('\n'.join(images).encode()).hexdigest()[:16]
    tags = sorted({version, *(alias for target, _ in items for alias in target['aliases'])})
    args = ['docker', 'buildx', 'imagetools', 'create', '--tag', f'{repository}:{version}-build{digest}']
    for tag in tags:
        args += ['--tag', repository + ':' + tag]
    subprocess.run([*args, *images], check=True)
