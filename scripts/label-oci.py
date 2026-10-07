#!/usr/bin/env python3
"""Attach organization repository metadata without changing the OCI rootfs."""
import hashlib
import json
import pathlib
import sys


def label(layout, metadata):
    blobs = layout / 'blobs/sha256'

    def read(descriptor):
        algorithm, digest = descriptor['digest'].split(':')
        if algorithm != 'sha256':
            raise ValueError('Unsupported OCI digest algorithm')
        return json.loads((blobs / digest).read_bytes())

    def replace(descriptor, obj):
        data = json.dumps(obj, separators=(',', ':')).encode()
        digest = hashlib.sha256(data).hexdigest()
        (blobs / digest).write_bytes(data)
        descriptor.update(digest='sha256:' + digest, size=len(data))

    index_path = layout / 'index.json'
    index = json.loads(index_path.read_bytes())
    for descriptor in index['manifests']:
        manifest = read(descriptor)
        config = read(manifest['config'])
        labels = config.setdefault('config', {}).setdefault('Labels', {})
        labels.update(metadata)
        replace(manifest['config'], config)
        replace(descriptor, manifest)
    index_path.write_text(json.dumps(index, separators=(',', ':')))


if __name__ == '__main__':
    label(pathlib.Path(sys.argv[1]), json.loads(pathlib.Path(sys.argv[2]).read_text()))
