#!/usr/bin/env bash
build_image() {
  run_builder bash /build-tools/centos/build-rootfs.sh
  publish_rootfs rootfs.tar.gz
}
