#!/usr/bin/env bash
# Build one discovered release and architecture on this runner.
run_builder() {
  docker run --rm --privileged --platform "$PLATFORM" \
    --mount "type=bind,src=$WORK/source,dst=/source,readonly" \
    --mount "type=bind,src=$WORK/context,dst=/output" \
    --mount "type=bind,src=$REPO_ROOT/scripts,dst=/build-tools/scripts,readonly" \
    --mount "type=bind,src=$REPO_ROOT/$lower,dst=/build-tools/$lower,readonly" \
    --env "VERSION=$VERSION" --env "SOURCE_DATE_EPOCH=$SOURCE_DATE_EPOCH" \
    "$BOOTSTRAP_ID" "$@"
}
metadata_hash() { sha256sum | cut -d' ' -f1; }
package_metadata() { run_builder /bin/sh /build-tools/scripts/package-metadata.sh | metadata_hash; }
publish_dockerfile() {
  local dockerfile=$1; shift
  local output=--push
  [[ "${VERIFY_ONLY:-false}" != true ]] || output=--load
  docker buildx build --progress=plain --platform "$PLATFORM" \
    --label "org.opencontainers.image.source=$source_label" \
    --label "org.opencontainers.image.url=$source_label" \
    --label "org.opencontainers.image.revision=$revision" \
    --file "$dockerfile" --tag "$reference" "$@" "$output" context
}
publish_rootfs() {
  local archive=$1 command=${2:-/bin/bash}
  test -s "context/$archive"
  printf 'FROM scratch\nADD %s /\nCMD ["%s"]\n' "$archive" "$command" > context/Dockerfile
  publish_dockerfile context/Dockerfile
}
publish_oci() {
  local archive=$1
  sudo apt-get update -qq
  sudo apt-get install -y -qq skopeo
  skopeo copy "oci-archive:$archive" "oci:$WORK/oci:base"
  python3 "$REPO_ROOT/scripts/label-oci.py" "$WORK/oci" "$source_label" "$revision"
  if [[ "${VERIFY_ONLY:-false}" == true ]]; then
    skopeo copy "oci:$WORK/oci:base" "docker-daemon:$reference"
  else
    skopeo copy --authfile "$HOME/.docker/config.json" "oci:$WORK/oci:base" "docker://$reference"
  fi
}
