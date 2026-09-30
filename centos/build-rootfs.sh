#!/usr/bin/env bash
set -euo pipefail

major=${1:?CentOS Stream major version is required}
[[ "$major" =~ ^[0-9]+$ ]]
base="/kickstarts/CentOS-Stream-$major-container-base.ks"
common="/kickstarts/CentOS-Stream-$major-container-common.ks"
test -s "$base"
test -s "$common"

# Use the package names and exclusions from the official container kickstarts.
mapfile -t packages < <(awk '
  /^%packages([[:space:]]|$)/ { in_packages=1; next }
  /^%end([[:space:]]|$)/ { in_packages=0; next }
  in_packages {
    sub(/[[:space:]]*#.*/, "")
    gsub(/^[[:space:]]+|[[:space:]]+$/, "")
    if ($0 != "" && $0 !~ /^-/) print $1
  }
' "$common" "$base" | sort -u)
mapfile -t exclusions < <(awk '
  /^%packages([[:space:]]|$)/ { in_packages=1; next }
  /^%end([[:space:]]|$)/ { in_packages=0; next }
  in_packages {
    sub(/[[:space:]]*#.*/, "")
    gsub(/^[[:space:]]+|[[:space:]]+$/, "")
    if ($0 ~ /^-/) { sub(/^-/, ""); print $1 }
  }
' "$common" "$base" | sort -u)
((${#packages[@]}))

mkdir -p /rootfs/etc/pki/rpm-gpg
cp -a /etc/pki/rpm-gpg/. /rootfs/etc/pki/rpm-gpg/
dnf_options=(
  --installroot=/rootfs "--releasever=$major"
  --setopt=reposdir=/etc/yum.repos.d
  --setopt=varsdir=/etc/dnf/vars
)
if grep -q '^%packages.*--excludedocs' "$base" "$common"; then
  dnf_options+=(--setopt=tsflags=nodocs)
fi
if grep -q '^%packages.*--excludeWeakdeps' "$base" "$common"; then
  dnf_options+=(--setopt=install_weak_deps=False)
fi
for package in "${exclusions[@]}"; do
  dnf_options+=("--exclude=$package")
done
dnf -y "${dnf_options[@]}" install "${packages[@]}"
dnf -y --installroot=/rootfs clean all

# Apply the container-specific cleanup from the mirrored kickstarts.
mkdir -p /rootfs/etc/systemd/system /rootfs/etc/rpm /rootfs/run/lock
for unit in systemd-logind.service getty.target console-getty.service \
  sys-fs-fuse-connections.mount systemd-remount-fs.service dev-hugepages.mount; do
  ln -sfn /dev/null "/rootfs/etc/systemd/system/$unit"
done
mkdir -p /rootfs/etc/pki
ln -sfn /run/secrets/etc-pki-entitlement /rootfs/etc/pki/entitlement-host
ln -sfn /run/secrets/rhsm /rootfs/etc/rhsm-host
printf '%%_install_langs C.utf8\n' > /rootfs/etc/rpm/macros.image-language-conf
printf 'LANG=C.utf8\n' > /rootfs/etc/locale.conf
rm -f /rootfs/etc/systemd/system/multi-user.target.wants/rhsmcertd.service
rm -f /rootfs/etc/sysconfig/network-scripts/ifcfg-*
rm -rf /rootfs/var/lib/dnf /rootfs/var/cache/* /rootfs/var/log/* /rootfs/tmp/*
: > /rootfs/etc/machine-id
chmod 0444 /rootfs/etc/machine-id

grep -qi 'CentOS' /rootfs/etc/os-release
