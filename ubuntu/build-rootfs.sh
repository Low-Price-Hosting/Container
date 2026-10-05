#!/usr/bin/env bash
set -euo pipefail
export DEBIAN_FRONTEND=noninteractive
apt-get update
apt-get install -y --no-install-recommends live-build debootstrap germinate \
  distro-info distro-info-data apt-utils ca-certificates gnupg git curl \
  python3 python3-apt python3-yaml python3-launchpadlib python3-click \
  jq sudo wget rsync attr gettext xz-utils grep-dctrl uuid-runtime
mkdir /recipe /work
cp -a /source/. /recipe/
ln -s /recipe /usr/share/livecd-rootfs
export LIVECD_ROOTFS_ROOT=/usr/share/livecd-rootfs
export PROJECT=ubuntu-oci SUBPROJECT=minimized IMAGEFORMAT=plain
export ARCH=$(dpkg --print-architecture)
SUITE=$( . /etc/os-release; echo "$VERSION_CODENAME" )
export SUITE
cd /work
ln -s /recipe/live-build/auto auto
# ubuntu-oci installs debootstrap's minimal set and does not consume seed
# tasks. Supply the supported germinate-cache marker to skip unrelated seeds.
mkdir -p config/germinate-output
touch config/germinate-output/structure
# The upstream OCI profile sets the minimal package set and container cleanup.
lb config --mode ubuntu --distribution "$SUITE" --architecture "$ARCH" --binary-images tar
lb build
cp livecd.ubuntu-oci.rootfs.tar.gz /output/rootfs.tar.gz
