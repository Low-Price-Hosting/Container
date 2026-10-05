#!/usr/bin/env bash
set -euo pipefail
dnf -y install python3 python3-pykickstart tar gzip
recipe="/source/container/rocky-container-base.ks"
[[ -f "$recipe" ]] || recipe="/source/Rocky-$VERSION-Container-Base.ks"
python3 /build-tools/scripts/kickstart-rootfs.py "$recipe" "$VERSION" /output/rootfs
tar --numeric-owner --xattrs -czf /output/rootfs.tar.gz -C /output/rootfs .
