#!/usr/bin/env bash
# Official KIWI Python installation for architectures without packaged KIWI.
set -euo pipefail
dnf -y --enablerepo=crb install \
  python3 python3-pip python3-lxml python3-pyyaml python3-requests \
  buildah skopeo rsync file lsof mtools openssl tar xz gzip zstd \
  util-linux attr policycoreutils microdnf
python3 -m venv --system-site-packages /opt/kiwi
/opt/kiwi/bin/python -m pip install --only-binary=:all: --no-deps --require-hashes \
  -r /build-tools/rockylinux/kiwi-requirements.txt
/opt/kiwi/bin/python -m pip install --no-deps --no-build-isolation --require-hashes \
  -r /build-tools/rockylinux/kiwi-source.txt
/opt/kiwi/bin/python -m pip check
/opt/kiwi/bin/python -c 'from importlib.metadata import version; assert version("kiwi") == "11.1.1"; print("Installed upstream KIWI " + version("kiwi"))'
