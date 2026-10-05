#!/bin/sh
set -eu
apk add --no-cache fakeroot tar gzip
ARCH=$(apk --print-arch)
export ARCH
. /source/scripts/mkimg.minirootfs.sh
profile_minirootfs
fakeroot /source/scripts/genrootfs.sh -a "$ARCH" -r /etc/apk/repositories \
  -k /etc/apk/keys -o /output/rootfs.tar.gz $rootfs_apks
