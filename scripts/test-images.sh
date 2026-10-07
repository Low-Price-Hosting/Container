#!/usr/bin/env bash
set -euo pipefail

distribution=${1:?Distribution is required}
references=${2:?Image reference list is required}
# A failed rerun must not retain an approval from an earlier test.
record="$RUNNER_TEMP/image.json"
jq '.tested=false | del(.os_version)' "$record" > "$record.tmp"
mv "$record.tmp" "$record"
[[ -s "$references" ]] || { echo "No local images were built for $distribution." >&2; exit 1; }

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
tested_os_version=
while IFS= read -r reference || [[ -n "$reference" ]]; do
  reference=${reference%$'\r'}
  [[ -n "$reference" ]] || continue
  echo "Smoke testing $reference"
  os_version=$(docker run --rm --pull=never --platform "${IMAGE_PLATFORM:?}" --entrypoint /bin/sh "$reference" -ec '
    . /etc/os-release
    test "$ID" = "$1"
    case "$ID" in
      ubuntu|debian) command -v apt-get >/dev/null ;;
      alpine) command -v apk >/dev/null ;;
      arch) command -v pacman >/dev/null ;;
      centos|fedora|almalinux|rocky)
        command -v dnf >/dev/null || command -v microdnf >/dev/null || command -v yum >/dev/null ;;
    esac
    printf "%s\n" "${VERSION_ID:-rolling}"
  ' smoke "$expected_id")
  [[ "$os_version" =~ ^[A-Za-z0-9][A-Za-z0-9._-]{0,63}$ ]] || {
    echo "Image returned an invalid VERSION_ID." >&2; exit 1;
  }
  [[ -z "$tested_os_version" || "$tested_os_version" == "$os_version" ]] || {
    echo "Local image versions disagree." >&2; exit 1;
  }
  tested_os_version=$os_version
  printf '%s %s\n' "$expected_id" "$os_version"
  architecture=${IMAGE_PLATFORM#linux/}
  architecture=${architecture%%/*}
  [[ "$(docker image inspect --format '{{.Architecture}}' "$reference")" == "$architecture" ]]
  [[ "$(docker image inspect --format '{{ index .Config.Labels "org.opencontainers.image.source" }}' "$reference")" == "$expected_source" ]]
done < "$references"
[[ -n "$tested_os_version" ]] || { echo "No local images were tested." >&2; exit 1; }

# The Publish job uses this result to approve the original build artifact.
jq --arg os_version "$tested_os_version" '.tested=true | .os_version=$os_version' "$record" > "$record.tmp"
mv "$record.tmp" "$record"
