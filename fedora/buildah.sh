#!/usr/bin/env bash
set -euo pipefail

case "${1:-}" in
  from|mount|umount|config|commit|rm|rmi) operation=$1 ;;
  *) operation=command ;;
esac

log_command() {
  if [[ -n ${OCI_COMMAND_LOG:-} ]]; then
    if { printf '%s\n' "$1" >> "$OCI_COMMAND_LOG"; } 2>/dev/null; then
      return 0
    fi
  fi
  printf '%s\n' "$1" >&2 || :
}

limit=10m
[[ $operation != commit ]] || limit=30m
started_seconds=$SECONDS
log_command "Buildah $operation: started"
status=0
timeout --kill-after=30s "$limit" /usr/bin/buildah "$@" || status=$?
log_command "Buildah $operation: finished status=$status duration=$((SECONDS - started_seconds))s"
exit "$status"
