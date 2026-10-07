#!/usr/bin/env bash
set -euo pipefail
REPO_ROOT=$(cd -- "$(dirname -- "$0")" && pwd)
: "${BUILD_TARGET:?The discovered build target is required}"
: "${RUNNER_TEMP:?}"
: "${PACKAGE_CACHE:?}"
DISTRIBUTION=$(jq -er .distribution <<< "$BUILD_TARGET")
VERSION=$(jq -er .version <<< "$BUILD_TARGET")
BOOTSTRAP=$(jq -er .bootstrap <<< "$BUILD_TARGET")
PLATFORM=$(jq -er .platform <<< "$BUILD_TARGET")
KEY=$(jq -er .key <<< "$BUILD_TARGET")
content_key=$(jq -er .fingerprint <<< "$BUILD_TARGET")
source_commit=$(jq -er .source_commit <<< "$BUILD_TARGET")
lower=$(tr '[:upper:]' '[:lower:]' <<< "$DISTRIBUTION")
image="ghcr.io/low-price-hosting/$lower"
source_label="https://github.com/Low-Price-Hosting/$DISTRIBUTION"
WORK=$(mktemp -d "$RUNNER_TEMP/container-build.XXXXXXXX")
cd "$WORK"
IMAGE_TEST_LIST="$RUNNER_TEMP/image-test-list.txt"
: > "$IMAGE_TEST_LIST"
git init --quiet source
git -C source remote add origin "$source_label.git"
# Pin the snapshot discovered for this run, even if Cron updates its branch meanwhile.
git -C source fetch --quiet --depth=1 origin "$source_commit"
git -C source checkout --quiet --detach FETCH_HEAD
jq -e --arg distro "$DISTRIBUTION" '.schema == 1 and .distribution == $distro' source/.container-source.json >/dev/null
revision=$(jq -er .revision source/.container-source.json)
SOURCE_DATE_EPOCH=$(git -C source show -s --format=%ct HEAD)
mkdir context
source "$REPO_ROOT/scripts/build-common.sh"
# The official image supplies build tools, not the final root filesystem.
docker pull --platform "$PLATFORM" "$BOOTSTRAP"
BOOTSTRAP_ID=$(docker image inspect --format '{{.Id}}' "$BOOTSTRAP")
source "$REPO_ROOT/$lower/build.sh"
[[ "$content_key" =~ ^[a-f0-9]{64}$ ]]
platform_tag=$(tr '/' '-' <<< "$PLATFORM")
immutable="$VERSION-$platform_tag-sha${content_key:0:16}"
reference="$image:$immutable"
build_image
printf '%s\n' "$reference" > "$IMAGE_TEST_LIST"
jq -n --arg key "$KEY" --arg platform "$PLATFORM" --arg image "$reference" --arg fingerprint "$content_key" \
  '{key:$key,platform:$platform,image:$image,fingerprint:$fingerprint,tested:false,pushed:false}' > "$RUNNER_TEMP/image.json"
