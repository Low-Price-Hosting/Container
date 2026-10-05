#!/usr/bin/env bash
build_image() {
  run_builder bash /build-tools/archlinux/build-rootfs.sh
  publish_dockerfile context/Dockerfile.base
}
