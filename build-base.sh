#!/usr/bin/env bash
set -euo pipefail
shopt -s nullglob

DISTRIBUTION="$1"
case "$DISTRIBUTION" in
  Alpine) script=alpine/build.sh ;;
  Debian) script=debian/build.sh ;;
  Fedora) script=fedora/build.sh ;;
  AlmaLinux) script=almalinux/build.sh ;;
  ArchLinux) script=archlinux/build.sh ;;
  RockyLinux) script=rockylinux/build.sh ;;
  Ubuntu) script=ubuntu/build.sh ;;
  Centos) script=centos/build.sh ;;
  *) echo "Unknown distribution: $DISTRIBUTION" >&2; exit 1 ;;
esac

REPO_ROOT=$(cd -- "$(dirname -- "$0")" && pwd)
org=Low-Price-Hosting
lower=$(printf '%s' "$DISTRIBUTION" | tr '[:upper:]' '[:lower:]')
image="ghcr.io/low-price-hosting/$lower"
mirror="https://github.com/$org/$DISTRIBUTION.git"
source_label="https://github.com/$org/$DISTRIBUTION"
: "$RUNNER_TEMP"
cd "$RUNNER_TEMP"
BUILD_ARGS=()

source "$REPO_ROOT/scripts/build-common.sh"
source "$REPO_ROOT/$script"
