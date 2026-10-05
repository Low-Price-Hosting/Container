#!/bin/sh
set -eu
# Hash repository metadata so package updates trigger a new rootfs.
if command -v apt-get >/dev/null; then
  apt-get update -qq >&2
  find /var/lib/apt/lists -maxdepth 1 -type f \( -name '*InRelease' -o -name '*Release' \) -exec sha256sum {} + | cut -d' ' -f1 | sort
elif command -v apk >/dev/null; then
  apk update >&2
  find /var/cache/apk -type f -name 'APKINDEX*' -exec sha256sum {} + | cut -d' ' -f1 | sort
elif command -v pacman >/dev/null; then
  pacman -Sy --noconfirm >&2
  find /var/lib/pacman/sync -type f -name '*.db' -exec sha256sum {} + | cut -d' ' -f1 | sort
else
  if command -v dnf >/dev/null; then manager=dnf; else manager=microdnf; fi
  "$manager" -q makecache --refresh >&2
  find /var/cache -type f -name repomd.xml -exec sha256sum {} + | cut -d' ' -f1 | sort
fi
