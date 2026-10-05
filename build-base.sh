#!/usr/bin/env bash
set -euo pipefail
REPO_ROOT=$(cd -- "$(dirname -- "$0")" && pwd)
: "${BUILD_TARGET:?The discovered build target is required}"
: "${RUNNER_TEMP:?}"
DISTRIBUTION=$(jq -er .distribution <<< "$BUILD_TARGET")
VERSION=$(jq -er .version <<< "$BUILD_TARGET")
BRANCH=$(jq -er .branch <<< "$BUILD_TARGET")
BOOTSTRAP=$(jq -er .bootstrap <<< "$BUILD_TARGET")
PLATFORM=$(jq -er .platform <<< "$BUILD_TARGET")
KEY=$(jq -er .key <<< "$BUILD_TARGET")
lower=$(tr '[:upper:]' '[:lower:]' <<< "$DISTRIBUTION")
image="ghcr.io/low-price-hosting/$lower"
source_label="https://github.com/Low-Price-Hosting/$DISTRIBUTION"
WORK=$(mktemp -d "$RUNNER_TEMP/container-build.XXXXXXXX")
cd "$WORK"
IMAGE_TEST_LIST="$RUNNER_TEMP/image-test-list.txt"
: > "$IMAGE_TEST_LIST"
git clone --quiet --depth=1 --single-branch --branch "$BRANCH" "$source_label.git" source
jq -e --arg distro "$DISTRIBUTION" '.schema == 1 and .distribution == $distro' source/.container-source.json >/dev/null
revision=$(jq -er .revision source/.container-source.json)
SOURCE_DATE_EPOCH=$(git -C source show -s --format=%ct HEAD)
mkdir context
source "$REPO_ROOT/scripts/build-common.sh"
# The official image supplies build tools, not the final root filesystem.
docker pull --platform "$PLATFORM" "$BOOTSTRAP"
BOOTSTRAP_ID=$(docker image inspect --format '{{.Id}}' "$BOOTSTRAP")
source "$REPO_ROOT/$lower/build.sh"
metadata=$(package_metadata)
[[ "$metadata" =~ ^[a-f0-9]{64}$ ]]
content_key=$({ printf '%s\n' "$revision" "$BOOTSTRAP_ID" "$PLATFORM" "$metadata"; git -C "$REPO_ROOT" rev-parse HEAD; } | sha256sum | cut -d' ' -f1)
platform_tag=$(tr '/' '-' <<< "$PLATFORM")
immutable="$VERSION-$platform_tag-sha${content_key:0:16}"
reference="$image:$immutable"
if [[ "${VERIFY_ONLY:-false}" != true ]] && docker buildx imagetools inspect "$reference" >/dev/null 2>&1; then
  echo "$reference already exists."
else
  build_image
fi
printf '%s\n' "$reference" > "$IMAGE_TEST_LIST"
jq -n --arg key "$KEY" --arg platform "$PLATFORM" --arg image "$reference" '{key:$key,platform:$platform,image:$image}' > "$RUNNER_TEMP/image.json"
