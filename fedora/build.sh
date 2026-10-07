#!/usr/bin/env bash
build_image() {
  run_builder bash /build-tools/fedora/build-rootfs.sh
  mapfile -t archives < <(find context/result-build -type f -name '*.oci.tar*')
  ((${#archives[@]} == 1))
  case "${archives[0]}" in
    *.xz) xz -dc "${archives[0]}" > context/image.oci.tar ;;
    *.gz) gzip -dc "${archives[0]}" > context/image.oci.tar ;;
    *) cp "${archives[0]}" context/image.oci.tar ;;
  esac
  load_oci context/image.oci.tar
}
