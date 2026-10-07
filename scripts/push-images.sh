#!/usr/bin/env bash
set -euo pipefail
record="$RUNNER_TEMP/image.json"
# Publication is possible only after the local image passed its runtime test.
jq -e '.tested == true and .pushed == false' "$record" >/dev/null
reference=$(jq -er .image "$record")
key=$(jq -er .key "$record")
fingerprint=$(jq -er .fingerprint "$record")
platform=$(jq -er .platform "$record")
for attempt in 1 2 3; do
  if docker push "$reference"; then
    break
  fi
  ((attempt < 3)) || exit 1
  echo "GHCR push failed; retrying ($attempt/3)" >&2
  sleep $((attempt * 5))
done

# Keep platform variants (arm/v6, arm/v7, amd64/v2) in the tested index.
# A Docker daemon's single-image push may omit the variant descriptor.
docker buildx imagetools inspect "$reference" --format '{{json .Manifest}}' > "$RUNNER_TEMP/pushed-manifest.json"
jq -e --arg platform "$platform" '
  ($platform | split("/")) as $parts |
  ({os:$parts[0],architecture:$parts[1]} + (if $parts[2] then {variant:$parts[2]} else {} end)) as $wanted |
  (if .manifests then
     [.manifests[] | select(.platform.os == $wanted.os and .platform.architecture == $wanted.architecture)][0]
   else . end) |
  select(.digest and .mediaType and .size) |
  {digest,mediaType,size,platform:$wanted}
' "$RUNNER_TEMP/pushed-manifest.json" > "$RUNNER_TEMP/tested-descriptor.json"
marker="${reference%%:*}:tested-$key-sha$fingerprint"
docker buildx imagetools create --annotation "index:io.low-price-hosting.build.inputs=$fingerprint" \
  --file "$RUNNER_TEMP/tested-descriptor.json" --tag "$marker"
digest=$(docker buildx imagetools inspect "$marker" --format '{{.Manifest.Digest}}')
[[ "$digest" =~ ^sha256:[a-f0-9]{64}$ ]]
jq --arg image "${reference%%:*}@$digest" '.image=$image | .pushed=true' "$record" > "$record.tmp"
mv "$record.tmp" "$record"
docker image rm --force "$reference" >/dev/null
