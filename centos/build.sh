#!/usr/bin/env bash
build_image() {
  run_builder bash /build-tools/centos/build-rootfs.sh
  build_rootfs rootfs.tar.gz
}
