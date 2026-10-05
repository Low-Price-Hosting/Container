#!/usr/bin/env bash
build_image() {
  run_builder /bin/sh /build-tools/alpine/build-rootfs.sh
  publish_rootfs rootfs.tar.gz /bin/sh
}
