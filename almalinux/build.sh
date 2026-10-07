#!/usr/bin/env bash
build_image() {
  mkdir -p "$PACKAGE_CACHE/dnf"
  python3 "$REPO_ROOT/almalinux/prepare-dockerfile.py" "source/Containerfiles/$VERSION/Containerfile.default" context/Dockerfile
  build_dockerfile context/Dockerfile --target container-image --build-arg "SYSBASE=$BOOTSTRAP" \
    --build-context "package-cache=$PACKAGE_CACHE"
  docker buildx build --platform "$PLATFORM" --file context/Dockerfile --target package-downloads \
    --build-arg "SYSBASE=$BOOTSTRAP" --build-context "package-cache=$PACKAGE_CACHE" \
    --output "type=local,dest=$WORK/downloaded-packages" context
  cp -a "$WORK/downloaded-packages/dnf/." "$PACKAGE_CACHE/dnf/"
}
