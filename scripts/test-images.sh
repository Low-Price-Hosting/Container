#!/usr/bin/env bash
set -euo pipefail

distribution=${1:?Distribution is required}
references=${2:?Image reference list is required}
[[ -s "$references" ]] || { echo "No images were published for $distribution." >&2; exit 1; }

case "$distribution" in
  Ubuntu) expected_id=ubuntu ;;
  Debian) expected_id=debian ;;
  Centos) expected_id=centos ;;
  Alpine) expected_id=alpine ;;
  Fedora) expected_id=fedora ;;
  AlmaLinux) expected_id=almalinux ;;
  ArchLinux) expected_id=arch ;;
  RockyLinux) expected_id=rocky ;;
  *) echo "Unknown distribution: $distribution" >&2; exit 1 ;;
esac

expected_source="https://github.com/Low-Price-Hosting/$distribution"
while IFS= read -r reference; do
  echo "Smoke testing $reference"
  if [[ "${LOCAL_ONLY:-false}" != true ]]; then
    docker buildx imagetools inspect "$reference" >/dev/null
  fi
  docker run --rm --platform "${IMAGE_PLATFORM:?}" --entrypoint /bin/sh "$reference" -ec '
    . /etc/os-release
    test "$ID" = "$1"
    case "$ID" in
      ubuntu|debian) command -v apt-get >/dev/null ;;
      alpine) command -v apk >/dev/null ;;
      arch) command -v pacman >/dev/null ;;
      centos|fedora|almalinux|rocky)
        command -v dnf >/dev/null || command -v microdnf >/dev/null || command -v yum >/dev/null ;;
    esac
    printf "%s %s\n" "$ID" "${VERSION_ID:-rolling}"
  ' smoke "$expected_id"
  architecture=${IMAGE_PLATFORM#linux/}
  architecture=${architecture%%/*}
  [[ "$(docker image inspect --format '{{.Architecture}}' "$reference")" == "$architecture" ]]
  [[ "$(docker image inspect --format '{{ index .Config.Labels "org.opencontainers.image.source" }}' "$reference")" == "$expected_source" ]]
  docker image rm --force "$reference" >/dev/null
done < "$references"
