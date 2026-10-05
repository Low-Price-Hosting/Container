#!/usr/bin/env bash
build_image() {
  run_builder bash /build-tools/rockylinux/build-rootfs.sh
  if [[ -f source/config.xml ]]; then
    mapfile -t archives < <(find context/result -type f -name '*.oci.tar*')
    ((${#archives[@]} == 1))
    case "${archives[0]}" in
      *.xz) xz -dc "${archives[0]}" > context/image.oci.tar ;;
      *.gz) gzip -dc "${archives[0]}" > context/image.oci.tar ;;
      *) cp "${archives[0]}" context/image.oci.tar ;;
    esac
    publish_oci context/image.oci.tar
  else
    publish_rootfs rootfs.tar.gz
  fi
}
