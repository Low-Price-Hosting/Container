#!/usr/bin/env bash
set -euo pipefail
major=${VERSION#stream}
dnf -y install python3 pykickstart tar gzip
python3 /build-tools/scripts/kickstart-rootfs.py \
  "/source/CentOS-Stream-$major-container-base.ks" "$major" /output/rootfs
tar --numeric-owner --xattrs -czf /output/rootfs.tar.gz -C /output/rootfs .
