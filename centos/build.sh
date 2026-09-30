#!/usr/bin/env bash
# Run through build-base.sh so shared image settings are available.
# Build from the mirrored Stream container kickstarts and the
# organization's previously published CentOS base image.
clone_branch main
mapfile -t releases < <(find source -maxdepth 1 -name 'CentOS-Stream-*-container-base.ks' \
  -printf '%f\n' | sed -nE 's/^CentOS-Stream-([0-9]+)-container-base\.ks$/\1/p' | sort -n)
((${#releases[@]}))
revision=$(git -C source rev-parse HEAD)
latest_major=
for major in "${releases[@]}"; do
  ((major >= 9)) || continue
  rm -rf context
  mkdir context
  cp "source/CentOS-Stream-$major-container-base.ks" context/
  cp "source/CentOS-Stream-$major-container-common.ks" context/
  cp "$REPO_ROOT/centos/Dockerfile" context/Dockerfile
  cp "$REPO_ROOT/centos/build-rootfs.sh" context/build-rootfs.sh
  builder_image="$image:stream$major"
  metadata_key=$(docker run --rm "$builder_image" bash -euo pipefail -c '
    dnf -q makecache --refresh >&2
    mapfile -d "" -t files < <(find /var/cache -type f -name repomd.xml -print0)
    ((${#files[@]}))
    sha256sum "${files[@]}" | awk "{print \$1}" | sort | sha256sum | cut -d" " -f1
  ')
  [[ "$metadata_key" =~ ^[0-9a-f]{64}$ ]]
  BUILD_CONTENT_KEY=$({
    printf '%s' "$revision"
    printf '%s' "$metadata_key"
    cat context/Dockerfile context/build-rootfs.sh
  } | sha256sum | cut -d' ' -f1)
  BUILD_ARGS=(--build-arg "CENTOS_MAJOR=$major" \
    --build-arg "CENTOS_BUILDER=$builder_image" \
    --build-arg "CENTOS_METADATA_KEY=$metadata_key")
  publish "stream$major" "$revision" context context/Dockerfile
  unset BUILD_CONTENT_KEY
  BUILD_ARGS=()
  latest_major=$major
done
[[ -n "$latest_major" ]]
publish_alias latest "stream$latest_major"
