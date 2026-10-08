#!/usr/bin/env bash
set -euo pipefail
dnf -y install kiwi kiwi-systemdeps distribution-gpg-keys
# Buildah runs inside Docker; use VFS instead of nested overlay storage.
export STORAGE_DRIVER=vfs
install -Dm755 /build-tools/fedora/buildah.sh /usr/local/libexec/fedora-oci/buildah
export PATH="/usr/local/libexec/fedora-oci:$PATH"
# KIWI captures command stderr; send progress directly to the builder log.
export OCI_COMMAND_LOG=/proc/1/fd/2
mkdir /recipe
cp -a /source/. /recipe/
cd /recipe
./kiwi-build --kiwi-file=Fedora.kiwi --image-type=oci \
  --image-profile=Container-Base-Generic --output-dir=/output/result
