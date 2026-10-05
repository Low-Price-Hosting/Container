#!/usr/bin/env bash
set -euo pipefail
pacman -Syu --noconfirm --needed devtools fakechroot fakeroot zstd make
mkdir /recipe
cp -a /source/. /recipe/
cd /recipe
export CI_COMMIT_SHA=$(cat .container-source.json | sed -n 's/.*"revision": "\([a-f0-9]*\)".*/\1/p')
# Original generators, restricted to the base profile.
scripts/make-rootfs.sh base /tmp/arch-rootfs /output "$(date -u -d 'yesterday' +%Y/%m/%d)" "$SOURCE_DATE_EPOCH"
scripts/make-dockerfile.sh base.tar.zst base /output true Base "$SOURCE_DATE_EPOCH"
