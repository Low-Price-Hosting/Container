#!/usr/bin/env python3
"""Retain upstream installroot stages and add a download-only cache export."""
import pathlib
import re
import sys

source = pathlib.Path(sys.argv[1]).read_text()
if 'FROM ${SYSBASE} AS system-build' not in source or 'RUN mkdir /mnt/sys-root;' not in source:
    raise RuntimeError('Upstream AlmaLinux build stages changed; review the cache adapter')
source = source.replace('RUN mkdir /mnt/sys-root;',
    'RUN --mount=type=bind,from=package-cache,target=/seed-cache,readonly '
    'mkdir -p /mnt/sys-root/var/cache/dnf; '
    'cp -a /seed-cache/dnf/. /mnt/sys-root/var/cache/dnf/;')
source = re.sub(r'\bdnf (install|reinstall)', r'dnf --setopt=keepcache=True \1', source)
cleanup = 'dnf --installroot /mnt/sys-root clean all;'
if cleanup not in source:
    raise RuntimeError('Upstream AlmaLinux package cleanup changed')
source = source.replace(cleanup, 'mkdir -p /saved-package-cache/dnf; '
    'cp -a /mnt/sys-root/var/cache/dnf/. /saved-package-cache/dnf/; ' + cleanup)
head, separator, tail = source.rpartition('FROM scratch\n')
if not separator:
    raise RuntimeError('Upstream AlmaLinux final stage must use scratch')
source = head + 'FROM scratch AS container-image\n' + tail
source += '\nFROM scratch AS package-downloads\nCOPY --from=system-build /saved-package-cache/ /\n'
pathlib.Path(sys.argv[2]).write_text(source)
