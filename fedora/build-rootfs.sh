#!/usr/bin/env bash
set -euo pipefail
dnf -y install kiwi kiwi-systemdeps distribution-gpg-keys
mkdir /recipe
cp -a /source/. /recipe/
cd /recipe
./kiwi-build --kiwi-file=Fedora.kiwi --image-type=oci \
  --image-profile=Container-Base-Generic --output-dir=/output/result
