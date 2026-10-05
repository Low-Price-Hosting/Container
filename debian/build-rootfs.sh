#!/usr/bin/env bash
set -euo pipefail
export DEBIAN_FRONTEND=noninteractive
apt-get update
apt-get install -y --no-install-recommends debootstrap debian-archive-keyring \
  ca-certificates wget gnupg gpgv xz-utils jq patch tar tzdata
export DEBUERREOTYPE_DIRECTORY=/source
export PATH="/source/scripts:$PATH"
mkdir -p /output/debuerreotype
bash /source/examples/debian.sh --arch "$(dpkg --print-architecture)" /output/debuerreotype "$VERSION" now
mapfile -t archives < <(find /output/debuerreotype -path "*/$VERSION/rootfs.tar.xz" -type f)
((${#archives[@]} == 1))
cp "${archives[0]}" /output/rootfs.tar.xz
