#!/usr/bin/env bash
set -euo pipefail
archive=${1:?Tested image archive is required}
record="$RUNNER_TEMP/image.json"
# Only the exact archive approved by the runtime test can be published.
jq -e '.tested == true and .pushed == false' "$record" >/dev/null
reference=$(jq -er .image "$record")
fingerprint=$(jq -er .fingerprint "$record")
platform=$(jq -er .platform "$record")
[[ "$fingerprint" =~ ^[a-f0-9]{64}$ ]]
checksum=$(sha256sum "$archive")
[[ "${checksum%% *}" == "$(jq -er .archive_sha256 "$record")" ]]
repository=${reference%%:*}
[[ "$repository" == ghcr.io/low-price-hosting/* ]]

# Upload by digest, keeping temporary architecture/cache tags out of the package.
crane="$RUNNER_TEMP/registry-tools/crane"
if [[ ! -x "$crane" ]]; then
  mkdir -p "${crane%/*}"
  tools_archive="${crane%/*}/crane.tar.gz"
  curl --fail --silent --show-error --location --retry 3 \
    https://github.com/google/go-containerregistry/releases/download/v0.22.1/go-containerregistry_Linux_x86_64.tar.gz \
    --output "$tools_archive"
  echo "0ab7a1d6932a213aed964ce97666c3077fe691c8606413674a8b3e0b9ec4cda0  $tools_archive" | sha256sum --check
  tar -xzf "$tools_archive" -C "${crane%/*}" crane
  rm "$tools_archive"
fi
# crane's Docker archive reader accepts an uncompressed tar file.
tarball="$RUNNER_TEMP/publish-image.tar"
trap 'rm -f "$tarball"' EXIT
gzip -dc "$archive" > "$tarball"
digest=$("$crane" digest --tarball "$tarball")
[[ "$digest" =~ ^sha256:[a-f0-9]{64}$ ]]
image="$repository@$digest"
for attempt in 1 2 3; do
  if "$crane" push "$tarball" "$image"; then
    break
  fi
  ((attempt < 3)) || exit 1
  echo "GHCR push failed; retrying ($attempt/3)" >&2
  sleep $((attempt * 5))
done

"$crane" manifest "$image" > "$RUNNER_TEMP/pushed-manifest.json"
manifest_checksum=$(sha256sum "$RUNNER_TEMP/pushed-manifest.json")
[[ "sha256:${manifest_checksum%% *}" == "$digest" ]]
manifest_size=$(wc -c < "$RUNNER_TEMP/pushed-manifest.json")
jq -e --arg image "$image" --arg digest "$digest" --arg platform "$platform" \
  --arg fingerprint "$fingerprint" --argjson size "$manifest_size" \
  --slurpfile manifest "$RUNNER_TEMP/pushed-manifest.json" '
  ($platform | split("/")) as $parts |
  select($parts[0] == "linux" and $parts[1] != "unknown") |
  $manifest[0].mediaType as $type |
  select($type == "application/vnd.oci.image.manifest.v1+json" or
         $type == "application/vnd.docker.distribution.manifest.v2+json") |
  .descriptor = {
    digest:$digest, mediaType:$type, size:$size,
    platform:({os:$parts[0],architecture:$parts[1]} + (if $parts[2] then {variant:$parts[2]} else {} end)),
    annotations:({"io.low-price-hosting.build.inputs":$fingerprint,"io.low-price-hosting.tested":"true"} +
      (if .os_version then {"io.low-price-hosting.os.version":.os_version} else {} end))
  } | .image=$image | .pushed=true
' "$record" > "$record.tmp"
mv "$record.tmp" "$record"
