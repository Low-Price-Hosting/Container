#!/usr/bin/env bash
set -euo pipefail
export DEBIAN_FRONTEND=noninteractive
apt-get update
apt-get install -y --no-install-recommends debootstrap debian-archive-keyring \
  ca-certificates wget gnupg gpgv xz-utils jq patch tar tzdata
# Some upstream stages invoke the apt helper by absolute path. Adapt a disposable
# copy so every stage gets the same bounded retries and visible update errors.
mkdir -p /recipe
cp -a /source/. /recipe/
mv /recipe/scripts/debuerreotype-apt-get /recipe/scripts/.upstream-debuerreotype-apt-get
install -m 0755 /build-tools/debian/snapshot-apt-get.sh /recipe/scripts/debuerreotype-apt-get
export DEBUERREOTYPE_DIRECTORY=/recipe
# Upstream inspects debootstrap itself for required features; use the real program.
export PATH="/recipe/scripts:${PACKAGE_ORIGINAL_PATH:-$PATH}"
mkdir -p /output/debuerreotype
bash /recipe/examples/debian.sh --arch "$(dpkg --print-architecture)" /output/debuerreotype "$VERSION" now
mapfile -t archives < <(find /output/debuerreotype -path "*/$VERSION/rootfs.tar.xz" -type f)
((${#archives[@]} == 1))
cp "${archives[0]}" /output/rootfs.tar.xz
