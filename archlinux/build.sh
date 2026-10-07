#!/usr/bin/env bash
build_image() {
  run_builder bash /build-tools/archlinux/build-rootfs.sh
  build_dockerfile context/Dockerfile.base
}
