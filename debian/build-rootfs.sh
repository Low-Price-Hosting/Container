#!/usr/bin/env bash
set -euo pipefail
export DEBIAN_FRONTEND=noninteractive
apt-get update
apt-get install -y --no-install-recommends debootstrap debian-archive-keyring \
  ca-certificates wget gnupg gpgv xz-utils jq patch tar tzdata
export DEBUERREOTYPE_DIRECTORY=/source
# Upstream inspects debootstrap itself for required features; use the real program.
export PATH="/source/scripts:${PACKAGE_ORIGINAL_PATH:-$PATH}"
# The upstream example updates its chroot through this command. Retry transient
# snapshot metadata failures there; builder-wide APT_CONFIG is not kept by chroot.
debuerreotype-apt-get() {
  if [[ "${2:-}" != update ]]; then
    command debuerreotype-apt-get "$@"
    return
  fi
  local rootfs=$1; shift 2
  local argument attempt status
  local arguments=()
  for argument do
    # Show the HTTP/signature failure instead of hiding it behind upstream -qq.
    case "$argument" in -q|-qq|--quiet|--quiet=2) continue;; esac
    arguments+=("$argument")
  done
  for attempt in 1 2 3; do
    echo "Snapshot APT update ($attempt/3)"
    status=0
    command debuerreotype-apt-get "$rootfs" -o Acquire::Retries=3 \
      -o Acquire::http::Timeout=60 -o Acquire::https::Timeout=60 \
      update "${arguments[@]}" || status=$?
    if (( status == 0 )); then return 0; fi
    if (( status != 100 || attempt == 3 )); then return "$status"; fi
    echo "Snapshot APT update failed (exit $status); retrying" >&2
    sleep "$(( attempt * 10 ))"
  done
}
export -f debuerreotype-apt-get
mkdir -p /output/debuerreotype
bash /source/examples/debian.sh --arch "$(dpkg --print-architecture)" /output/debuerreotype "$VERSION" now
mapfile -t archives < <(find /output/debuerreotype -path "*/$VERSION/rootfs.tar.xz" -type f)
((${#archives[@]} == 1))
cp "${archives[0]}" /output/rootfs.tar.xz
