#!/usr/bin/env bash
set -euo pipefail
if [[ -f /source/config.xml ]]; then
  dnf -y install rocky-release-core
  if (( VERSION >= 10 )); then
    # The upstream README documents EPEL for current KIWI and its hook lifecycle.
    # These packages install in the disposable builder, not in the image rootfs.
    dnf -y install epel-release
    dnf -y --enablerepo=crb install kiwi-cli kiwi-systemdeps-containers kiwi-systemdeps-core distribution-gpg-keys
  else
    dnf -y --enablerepo='*core*' install kiwi-cli kiwi-systemdeps-containers kiwi-systemdeps-core
  fi
  mkdir /recipe
  cp -a /source/. /recipe/
  cd /recipe
  export TERM=xterm
  ./container-build.sh --container Base --output-dir /output/result
  exit 0
fi
dnf -y install python3 pykickstart tar gzip
recipe="/source/container/rocky-container-base.ks"
[[ -f "$recipe" ]] || recipe="/source/Rocky-$VERSION-Container-Base.ks"
python3 /build-tools/scripts/kickstart-rootfs.py "$recipe" "$VERSION" /output/rootfs
tar --numeric-owner --xattrs -czf /output/rootfs.tar.gz -C /output/rootfs .
