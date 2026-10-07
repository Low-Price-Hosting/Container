#!/usr/bin/env bash
build_image() {
  run_builder /bin/sh /build-tools/alpine/build-rootfs.sh
  build_rootfs rootfs.tar.gz /bin/sh
}
