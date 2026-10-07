#!/usr/bin/env bash
# Build one discovered release and architecture on this runner.
run_builder() {
  docker run --rm --privileged --platform "$PLATFORM" \
    --mount "type=bind,src=$WORK/source,dst=/source,readonly" \
    --mount "type=bind,src=$WORK/context,dst=/output" \
    --mount "type=bind,src=$REPO_ROOT/scripts,dst=/build-tools/scripts,readonly" \
    --mount "type=bind,src=$REPO_ROOT/$lower,dst=/build-tools/$lower,readonly" \
    --mount "type=bind,src=$PACKAGE_CACHE,dst=/package-cache" \
    --env "VERSION=$VERSION" --env "SOURCE_DATE_EPOCH=$SOURCE_DATE_EPOCH" \
    "$BOOTSTRAP_ID" /bin/sh /build-tools/scripts/package-cache.sh "$@"
}
build_dockerfile() {
  local dockerfile=$1; shift
  local label labels=()
  while IFS= read -r label; do
    labels+=(--label "$label")
  done < <(jq -r 'to_entries[] | "\(.key)=\(.value)"' "$IMAGE_LABELS")
  docker buildx build --progress=plain --platform "$PLATFORM" \
    "${labels[@]}" \
    --file "$dockerfile" --tag "$reference" "$@" --load context
}
build_rootfs() {
  local archive=$1 command=${2:-/bin/bash}
  test -s "context/$archive"
  printf 'FROM scratch\nADD %s /\nCMD ["%s"]\n' "$archive" "$command" > context/Dockerfile
  build_dockerfile context/Dockerfile
}
load_oci() {
  local archive=$1
  sudo apt-get update -qq
  sudo apt-get install -y -qq skopeo
  skopeo copy "oci-archive:$archive" "oci:$WORK/oci:base"
  python3 "$REPO_ROOT/scripts/label-oci.py" "$WORK/oci" "$IMAGE_LABELS"
  skopeo copy "oci:$WORK/oci:base" "docker-daemon:$reference"
}
