#!/usr/bin/env bash
# Keep the official chroot/keyring handling and retry only its metadata update.
set -euo pipefail
upstream="$(dirname "$(readlink -vf "$BASH_SOURCE")")/.upstream-debuerreotype-apt-get"
if [[ "${2:-}" != update ]]; then
  exec "$upstream" "$@"
fi
rootfs=$1; shift 2
arguments=()
for argument do
  # Show HTTP/signature errors instead of hiding them behind upstream -qq.
  case "$argument" in -q|-qq|--quiet|--quiet=2) continue;; esac
  arguments+=("$argument")
done
for attempt in 1 2 3; do
  echo "Snapshot APT update ($attempt/3)"
  status=0
  "$upstream" "$rootfs" -o Acquire::Retries=3 \
    -o Acquire::http::Timeout=60 -o Acquire::https::Timeout=60 \
    update "${arguments[@]}" || status=$?
  if (( status == 0 )); then exit 0; fi
  if (( status != 100 || attempt == 3 )); then exit "$status"; fi
  echo "Snapshot APT update failed (exit $status); retrying" >&2
  sleep "$(( attempt * 10 ))"
done
