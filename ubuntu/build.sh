#!/usr/bin/env bash
build_image() {
  run_builder bash /build-tools/ubuntu/build-rootfs.sh
  build_rootfs rootfs.tar.gz
}
