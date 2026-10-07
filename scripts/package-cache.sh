#!/bin/sh
# Cache downloads only. Package managers still refresh indexes and verify packages.
set -eu
if [ "${1:-}" = --prune ]; then
  python3 - <<'PY'
import os, pathlib
root = pathlib.Path(os.environ['PACKAGE_CACHE']).resolve()
assert root.is_relative_to(pathlib.Path(os.environ['RUNNER_TEMP']).resolve())
files = []
for path in root.rglob('*'):
    if path.is_symlink():
        path.unlink()
    elif path.is_file():
        if path.name.endswith(('.deb', '.rpm', '.apk', '.pkg.tar.zst', '.pkg.tar.xz', '.sig')):
            files.append(path)
        else:
            path.unlink()
size = sum(p.stat().st_size for p in files)
for path in sorted(files, key=lambda p: p.stat().st_mtime):
    if size <= 64 * 1024 * 1024:
        break
    size -= path.stat().st_size
    path.unlink()
print(f'Package download cache: {size / 1024 / 1024:.1f} MiB (limit 64 MiB)')
PY
  exit 0
fi
tool=${0##*/}
if [ "$tool" != package-cache.sh ]; then
  real=$(PATH="$PACKAGE_ORIGINAL_PATH" command -v "$tool")
  root=
  previous=
  clean=false
  for argument do
    case "$previous" in --installroot|--root|-r) root=$argument;; esac
    case "$argument" in
      --installroot=*|--root=*) root=${argument#*=};;
      clean) clean=true;;
    esac
    previous=$argument
  done
  mounted=
  case "$tool" in
    debootstrap) exec "$real" --cache-dir=/package-cache/apt "$@";;
    dnf|dnf5|microdnf)
      if [ -n "$root" ] && [ "$clean" = false ]; then
        mounted="$root/var/cache/dnf"
        mkdir -p "$mounted"
        mount --bind /package-cache/dnf "$mounted"
      fi
      set -- --setopt=keepcache=True "$@"
      ;;
    apk)
      # Upstream genrootfs uses --no-cache. Replace only its download policy.
      count=$#
      while [ "$count" -gt 0 ]; do
        argument=$1; shift; count=$((count - 1))
        [ "$argument" = --no-cache ] || set -- "$@" "$argument"
      done
      if [ -n "$root" ]; then
        mounted="$root/var/cache/apk"
        mkdir -p "$mounted"
        mount --bind /package-cache/apk "$mounted"
      fi
      set -- --cache-dir=/var/cache/apk --update-cache "$@"
      ;;
    pacman) set -- --cachedir /package-cache/pacman "$@";;
  esac
  status=0
  "$real" "$@" || status=$?
  if [ -n "$mounted" ]; then umount "$mounted"; fi
  exit "$status"
fi

mkdir -p /package-cache/apt/partial /package-cache/apk /package-cache/dnf /package-cache/pacman /package-cache/kiwi
export PACKAGE_ORIGINAL_PATH=$PATH
wrappers=/usr/local/libexec/container-package-cache
mkdir -p "$wrappers"
for manager in debootstrap apk dnf dnf5 microdnf pacman; do
  ln -s /build-tools/scripts/package-cache.sh "$wrappers/$manager"
done
if command -v apt-get >/dev/null; then
  rm -f /etc/apt/apt.conf.d/docker-clean
  printf 'Dir::Cache::archives "/package-cache/apt";\nBinary::apt::APT::Keep-Downloaded-Packages "true";\nAPT::Keep-Downloaded-Packages "true";\n' > /etc/apt/apt.conf.d/99container-package-cache
fi
if command -v apk >/dev/null; then
  mkdir -p /var/cache/apk
  mount --bind /package-cache/apk /var/cache/apk
fi
if command -v dnf >/dev/null || command -v dnf5 >/dev/null || command -v microdnf >/dev/null; then
  mkdir -p /var/cache/dnf /var/cache/kiwi
  mount --bind /package-cache/dnf /var/cache/dnf
  mount --bind /package-cache/kiwi /var/cache/kiwi
fi
export PATH="$wrappers:$PATH"
exec "$@"
