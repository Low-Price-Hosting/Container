#!/usr/bin/env bash
build_image() {
  run_builder bash /build-tools/debian/build-rootfs.sh
  publish_rootfs rootfs.tar.xz
}
