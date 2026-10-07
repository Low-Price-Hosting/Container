#!/usr/bin/env bash
set -euo pipefail

mode=${1:?Use save or restore}
directory=${2:?Image artifact directory is required}
: "${RUNNER_TEMP:?}"
record="$RUNNER_TEMP/image.json"

case "$mode" in
  save)
    reference=$(jq -er .image "$record")
    [[ "$(cat "$RUNNER_TEMP/image-test-list.txt")" == "$reference" ]]
    mkdir -p "$directory"
    docker save "$reference" | gzip -1 > "$directory/image.tar.gz.tmp"
    mv "$directory/image.tar.gz.tmp" "$directory/image.tar.gz"
    checksum=$(sha256sum "$directory/image.tar.gz")
    checksum=${checksum%% *}
    jq --arg checksum "$checksum" '.archive_sha256=$checksum' "$record" > "$record.tmp"
    mv "$record.tmp" "$record"
    cp "$record" "$directory/image.json"
    cp "$RUNNER_TEMP/image-test-list.txt" "$directory/image-test-list.txt"
    ;;
  restore)
    checksum=$(jq -er .archive_sha256 "$directory/image.json")
    [[ "$checksum" =~ ^[a-f0-9]{64}$ ]]
    actual=$(sha256sum "$directory/image.tar.gz")
    [[ "${actual%% *}" == "$checksum" ]] || { echo 'Image archive checksum mismatch.' >&2; exit 1; }
    reference=$(jq -er .image "$directory/image.json")
    [[ "$(cat "$directory/image-test-list.txt")" == "$reference" ]]
    gzip -dc "$directory/image.tar.gz" | docker load
    cp "$directory/image.json" "$record"
    cp "$directory/image-test-list.txt" "$RUNNER_TEMP/image-test-list.txt"
    ;;
  *) echo 'Use save or restore.' >&2; exit 1 ;;
esac
