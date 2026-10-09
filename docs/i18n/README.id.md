<div align="center">

**🌐 Bahasa**

[Türkçe](../../README.md) · [English](README.en.md) · [简体中文](README.zh-CN.md) · [繁體中文](README.zh-TW.md) · [日本語](README.ja.md) · [한국어](README.ko.md)

[Deutsch](README.de.md) · [Français](README.fr.md) · [Español](README.es.md) · [Português (Brasil)](README.pt-BR.md) · [Italiano](README.it.md) · [Русский](README.ru.md)

[Українська](README.uk.md) · [العربية](README.ar.md) · [فارسی](README.fa.md) · [हिन्दी](README.hi.md) · **Bahasa Indonesia** · [Tiếng Việt](README.vi.md)

</div>

---

# Low-Price-Hosting · Container

**Image dasar Linux untuk container — dibangun dari resep sumber, diuji per arsitektur, dan dipublikasikan ke GHCR, Docker Hub, dan Quay.**

[![Status pembangunan](https://github.com/Low-Price-Hosting/Container/actions/workflows/build-base-images.yml/badge.svg?branch=main)](https://github.com/Low-Price-Hosting/Container/actions/workflows/build-base-images.yml)
[![Pembaruan sumber](https://github.com/Low-Price-Hosting/Cron/actions/workflows/mirror-container-sources.yml/badge.svg?branch=main)](https://github.com/Low-Price-Hosting/Cron/actions/workflows/mirror-container-sources.yml)
[![Registri: GHCR](https://img.shields.io/badge/registry-GHCR-0969da?style=flat-square)](https://github.com/orgs/Low-Price-Hosting/packages?ecosystem=container)
[![Registri: Docker Hub](https://img.shields.io/badge/registry-Docker_Hub-2496ed?style=flat-square)](https://hub.docker.com/u/lphllc)
[![Registri: Quay](https://img.shields.io/badge/registry-Quay-ee0000?style=flat-square)](https://quay.io/organization/lowpricehosting)

**8 distribusi** · **Versi dan arsitektur dinamis** · **Bangun → Uji → Publikasikan**

[Image](#images-and-downloads) · [Arsitektur](#versions-and-architectures) · [Penggunaan](#quick-start) · [Memulai pembangunan](#run-builds) · [Informasi image](#oci-metadata)

---

<a id="images-and-downloads"></a>

## Image dan unduhan

| Distribusi | GHCR | Docker Hub | Quay |
|---|---|---|---|
| [Ubuntu](https://github.com/Low-Price-Hosting/Ubuntu) | [![ubuntu jumlah unduhan GHCR](https://img.shields.io/badge/dynamic/regex?url=https%3A%2F%2Fgithub.com%2Forgs%2FLow-Price-Hosting%2Fpackages%2Fcontainer%2Fpackage%2Fubuntu&search=Total%20downloads%3C%2Fspan%3E%5Cs%2A%3Ch3%20title%3D%22%28%5B0-9%2C%5D%2B%29%22%3E&replace=%241&label=GHCR%20downloads&color=0969da&style=flat-square&cacheSeconds=300)](https://github.com/orgs/Low-Price-Hosting/packages/container/package/ubuntu) | [![ubuntu Docker Hub pulls](https://img.shields.io/docker/pulls/lphllc/ubuntu?label=Docker%20pulls&style=flat-square)](https://hub.docker.com/r/lphllc/ubuntu) | [![ubuntu Quay architectures](https://img.shields.io/badge/dynamic/json?url=https%3A%2F%2Fquay.io%2Fapi%2Fv1%2Frepository%2Flowpricehosting%2Fubuntu%2Ftag%2F%3FspecificTag%3Dlatest%26onlyActiveTags%3Dtrue&query=%24.tags%5B0%5D.child_manifest_count&label=Quay%20architectures&color=ee0000&style=flat-square&cacheSeconds=300)](https://quay.io/repository/lowpricehosting/ubuntu?tab=tags) |
| [Debian](https://github.com/Low-Price-Hosting/Debian) | [![debian jumlah unduhan GHCR](https://img.shields.io/badge/dynamic/regex?url=https%3A%2F%2Fgithub.com%2Forgs%2FLow-Price-Hosting%2Fpackages%2Fcontainer%2Fpackage%2Fdebian&search=Total%20downloads%3C%2Fspan%3E%5Cs%2A%3Ch3%20title%3D%22%28%5B0-9%2C%5D%2B%29%22%3E&replace=%241&label=GHCR%20downloads&color=0969da&style=flat-square&cacheSeconds=300)](https://github.com/orgs/Low-Price-Hosting/packages/container/package/debian) | [![debian Docker Hub pulls](https://img.shields.io/docker/pulls/lphllc/debian?label=Docker%20pulls&style=flat-square)](https://hub.docker.com/r/lphllc/debian) | [![debian Quay architectures](https://img.shields.io/badge/dynamic/json?url=https%3A%2F%2Fquay.io%2Fapi%2Fv1%2Frepository%2Flowpricehosting%2Fdebian%2Ftag%2F%3FspecificTag%3Dlatest%26onlyActiveTags%3Dtrue&query=%24.tags%5B0%5D.child_manifest_count&label=Quay%20architectures&color=ee0000&style=flat-square&cacheSeconds=300)](https://quay.io/repository/lowpricehosting/debian?tab=tags) |
| [CentOS Stream](https://github.com/Low-Price-Hosting/Centos) | [![centos jumlah unduhan GHCR](https://img.shields.io/badge/dynamic/regex?url=https%3A%2F%2Fgithub.com%2Forgs%2FLow-Price-Hosting%2Fpackages%2Fcontainer%2Fpackage%2Fcentos&search=Total%20downloads%3C%2Fspan%3E%5Cs%2A%3Ch3%20title%3D%22%28%5B0-9%2C%5D%2B%29%22%3E&replace=%241&label=GHCR%20downloads&color=0969da&style=flat-square&cacheSeconds=300)](https://github.com/orgs/Low-Price-Hosting/packages/container/package/centos) | [![centos Docker Hub pulls](https://img.shields.io/docker/pulls/lphllc/centos?label=Docker%20pulls&style=flat-square)](https://hub.docker.com/r/lphllc/centos) | [![centos Quay architectures](https://img.shields.io/badge/dynamic/json?url=https%3A%2F%2Fquay.io%2Fapi%2Fv1%2Frepository%2Flowpricehosting%2Fcentos%2Ftag%2F%3FspecificTag%3Dlatest%26onlyActiveTags%3Dtrue&query=%24.tags%5B0%5D.child_manifest_count&label=Quay%20architectures&color=ee0000&style=flat-square&cacheSeconds=300)](https://quay.io/repository/lowpricehosting/centos?tab=tags) |
| [Alpine](https://github.com/Low-Price-Hosting/Alpine) | [![alpine jumlah unduhan GHCR](https://img.shields.io/badge/dynamic/regex?url=https%3A%2F%2Fgithub.com%2Forgs%2FLow-Price-Hosting%2Fpackages%2Fcontainer%2Fpackage%2Falpine&search=Total%20downloads%3C%2Fspan%3E%5Cs%2A%3Ch3%20title%3D%22%28%5B0-9%2C%5D%2B%29%22%3E&replace=%241&label=GHCR%20downloads&color=0969da&style=flat-square&cacheSeconds=300)](https://github.com/orgs/Low-Price-Hosting/packages/container/package/alpine) | [![alpine Docker Hub pulls](https://img.shields.io/docker/pulls/lphllc/alpine?label=Docker%20pulls&style=flat-square)](https://hub.docker.com/r/lphllc/alpine) | [![alpine Quay architectures](https://img.shields.io/badge/dynamic/json?url=https%3A%2F%2Fquay.io%2Fapi%2Fv1%2Frepository%2Flowpricehosting%2Falpine%2Ftag%2F%3FspecificTag%3Dlatest%26onlyActiveTags%3Dtrue&query=%24.tags%5B0%5D.child_manifest_count&label=Quay%20architectures&color=ee0000&style=flat-square&cacheSeconds=300)](https://quay.io/repository/lowpricehosting/alpine?tab=tags) |
| [Fedora](https://github.com/Low-Price-Hosting/Fedora) | [![fedora jumlah unduhan GHCR](https://img.shields.io/badge/dynamic/regex?url=https%3A%2F%2Fgithub.com%2Forgs%2FLow-Price-Hosting%2Fpackages%2Fcontainer%2Fpackage%2Ffedora&search=Total%20downloads%3C%2Fspan%3E%5Cs%2A%3Ch3%20title%3D%22%28%5B0-9%2C%5D%2B%29%22%3E&replace=%241&label=GHCR%20downloads&color=0969da&style=flat-square&cacheSeconds=300)](https://github.com/orgs/Low-Price-Hosting/packages/container/package/fedora) | [![fedora Docker Hub pulls](https://img.shields.io/docker/pulls/lphllc/fedora?label=Docker%20pulls&style=flat-square)](https://hub.docker.com/r/lphllc/fedora) | [![fedora Quay architectures](https://img.shields.io/badge/dynamic/json?url=https%3A%2F%2Fquay.io%2Fapi%2Fv1%2Frepository%2Flowpricehosting%2Ffedora%2Ftag%2F%3FspecificTag%3Dlatest%26onlyActiveTags%3Dtrue&query=%24.tags%5B0%5D.child_manifest_count&label=Quay%20architectures&color=ee0000&style=flat-square&cacheSeconds=300)](https://quay.io/repository/lowpricehosting/fedora?tab=tags) |
| [AlmaLinux](https://github.com/Low-Price-Hosting/AlmaLinux) | [![almalinux jumlah unduhan GHCR](https://img.shields.io/badge/dynamic/regex?url=https%3A%2F%2Fgithub.com%2Forgs%2FLow-Price-Hosting%2Fpackages%2Fcontainer%2Fpackage%2Falmalinux&search=Total%20downloads%3C%2Fspan%3E%5Cs%2A%3Ch3%20title%3D%22%28%5B0-9%2C%5D%2B%29%22%3E&replace=%241&label=GHCR%20downloads&color=0969da&style=flat-square&cacheSeconds=300)](https://github.com/orgs/Low-Price-Hosting/packages/container/package/almalinux) | [![almalinux Docker Hub pulls](https://img.shields.io/docker/pulls/lphllc/almalinux?label=Docker%20pulls&style=flat-square)](https://hub.docker.com/r/lphllc/almalinux) | [![almalinux Quay architectures](https://img.shields.io/badge/dynamic/json?url=https%3A%2F%2Fquay.io%2Fapi%2Fv1%2Frepository%2Flowpricehosting%2Falmalinux%2Ftag%2F%3FspecificTag%3Dlatest%26onlyActiveTags%3Dtrue&query=%24.tags%5B0%5D.child_manifest_count&label=Quay%20architectures&color=ee0000&style=flat-square&cacheSeconds=300)](https://quay.io/repository/lowpricehosting/almalinux?tab=tags) |
| [Arch Linux](https://github.com/Low-Price-Hosting/ArchLinux) | [![archlinux jumlah unduhan GHCR](https://img.shields.io/badge/dynamic/regex?url=https%3A%2F%2Fgithub.com%2Forgs%2FLow-Price-Hosting%2Fpackages%2Fcontainer%2Fpackage%2Farchlinux&search=Total%20downloads%3C%2Fspan%3E%5Cs%2A%3Ch3%20title%3D%22%28%5B0-9%2C%5D%2B%29%22%3E&replace=%241&label=GHCR%20downloads&color=0969da&style=flat-square&cacheSeconds=300)](https://github.com/orgs/Low-Price-Hosting/packages/container/package/archlinux) | [![archlinux Docker Hub pulls](https://img.shields.io/docker/pulls/lphllc/archlinux?label=Docker%20pulls&style=flat-square)](https://hub.docker.com/r/lphllc/archlinux) | [![archlinux Quay architectures](https://img.shields.io/badge/dynamic/json?url=https%3A%2F%2Fquay.io%2Fapi%2Fv1%2Frepository%2Flowpricehosting%2Farchlinux%2Ftag%2F%3FspecificTag%3Dlatest%26onlyActiveTags%3Dtrue&query=%24.tags%5B0%5D.child_manifest_count&label=Quay%20architectures&color=ee0000&style=flat-square&cacheSeconds=300)](https://quay.io/repository/lowpricehosting/archlinux?tab=tags) |
| [Rocky Linux](https://github.com/Low-Price-Hosting/RockyLinux) | [![rockylinux jumlah unduhan GHCR](https://img.shields.io/badge/dynamic/regex?url=https%3A%2F%2Fgithub.com%2Forgs%2FLow-Price-Hosting%2Fpackages%2Fcontainer%2Fpackage%2Frockylinux&search=Total%20downloads%3C%2Fspan%3E%5Cs%2A%3Ch3%20title%3D%22%28%5B0-9%2C%5D%2B%29%22%3E&replace=%241&label=GHCR%20downloads&color=0969da&style=flat-square&cacheSeconds=300)](https://github.com/orgs/Low-Price-Hosting/packages/container/package/rockylinux) | [![rockylinux Docker Hub pulls](https://img.shields.io/docker/pulls/lphllc/rockylinux?label=Docker%20pulls&style=flat-square)](https://hub.docker.com/r/lphllc/rockylinux) | [![rockylinux Quay architectures](https://img.shields.io/badge/dynamic/json?url=https%3A%2F%2Fquay.io%2Fapi%2Fv1%2Frepository%2Flowpricehosting%2Frockylinux%2Ftag%2F%3FspecificTag%3Dlatest%26onlyActiveTags%3Dtrue&query=%24.tags%5B0%5D.child_manifest_count&label=Quay%20architectures&color=ee0000&style=flat-square&cacheSeconds=300)](https://quay.io/repository/lowpricehosting/rockylinux?tab=tags) |

Lencana GHCR dan Docker Hub menampilkan total unduhan; lencana Quay menampilkan jumlah arsitektur untuk tag `latest`. Klik lencana untuk melihat tag dan arsitektur. Penghitung berlaku untuk masing-masing registry; cache dapat menunda pembaruan.

```bash
docker pull ghcr.io/low-price-hosting/ubuntu:latest
docker pull docker.io/lphllc/ubuntu:latest
docker pull quay.io/lowpricehosting/ubuntu:latest
```

<a id="versions-and-architectures"></a>

## Referensi versi dan arsitektur

Referensi versi dan arsitektur dari [rencana penemuan tanggal 8 Oktober 2026](https://github.com/Low-Price-Hosting/Container/actions/runs/37741062225). Ini adalah target yang ditemukan; periksa arsitektur yang telah dipublikasikan pada kolom **OS/Arch** dari tag yang dipilih atau pada indeks OCI.

| Distribusi | Versi | Platform — dengan awalan `linux/` |
|---|---|---|
| Ubuntu | `22.04`, `24.04`, `26.04` | `amd64`, `arm/v7`, `arm64`, `ppc64le`, `riscv64`, `s390x` |
| Debian | `bookworm` | `386`, `amd64`, `arm/v7`, `arm64`, `ppc64le` |
| Debian | `trixie` | `386`, `amd64`, `arm/v5`, `arm/v7`, `arm64`, `ppc64le`, `riscv64`, `s390x` |
| CentOS Stream | `stream9`, `stream10` | `amd64`, `arm64`, `ppc64le`, `s390x` |
| Alpine | `3.21`, `3.22`, `3.23`, `3.24` | `386`, `amd64`, `arm/v6`, `arm/v7`, `arm64`, `ppc64le`, `riscv64`, `s390x` |
| Fedora | `43`, `44` | `amd64`, `arm64`, `ppc64le`, `s390x` |
| AlmaLinux | `8`, `9` | `386`, `amd64`, `arm64`, `ppc64le`, `s390x` |
| AlmaLinux | `10` | `386`, `amd64`, `amd64/v2`, `arm64`, `ppc64le`, `s390x` |
| Arch Linux | `rolling` | `amd64` |
| Rocky Linux | `8` | `amd64`, `arm64` |
| Rocky Linux | `9` | `amd64`, `arm64`, `ppc64le`, `s390x` |
| Rocky Linux | `10` | `amd64`, `arm64`, `ppc64le`, `riscv64`, `s390x` |

Kumpulan arsitektur dapat berbeda menurut versi.

Periksa arsitektur sebenarnya dari suatu tag:

```bash
docker buildx imagetools inspect ghcr.io/low-price-hosting/ubuntu:latest
docker buildx imagetools inspect --raw ghcr.io/low-price-hosting/ubuntu:latest
```

<a id="quick-start"></a>

## Penggunaan cepat

Ganti `latest` dalam contoh dengan **tag yang telah dipublikasikan** yang ingin Anda gunakan. Anda tidak perlu masuk ke GHCR untuk mengunduh image publik.

### Unduh dan jalankan

```bash
docker pull ghcr.io/low-price-hosting/ubuntu:latest
docker run --rm -it ghcr.io/low-price-hosting/ubuntu:latest /bin/sh
```

Docker memilih image dari tag multiarsitektur yang sesuai dengan arsitektur komputer Anda.

### Pilih arsitektur

```bash
docker pull --platform linux/arm64 ghcr.io/low-price-hosting/ubuntu:latest

docker run --rm --platform linux/arm64 \
  ghcr.io/low-price-hosting/ubuntu:latest \
  /bin/sh -c 'cat /etc/os-release'
```

Untuk menjalankan image dari keluarga prosesor yang berbeda, diperlukan emulasi yang sesuai.

### Tetapkan menggunakan digest

```bash
docker image inspect --format '{{json .RepoDigests}}' \
  ghcr.io/low-price-hosting/ubuntu:latest

# Ganti <digest> dengan nilai SHA256 image.
docker pull ghcr.io/low-price-hosting/ubuntu@sha256:<digest>
```

Tag versi dapat diperbarui; digest memungkinkan Anda menggunakan kembali image yang sama.

### Gunakan dalam image Anda sendiri

```dockerfile
FROM ghcr.io/low-price-hosting/ubuntu:latest

COPY app/ /opt/app/
WORKDIR /opt/app
CMD ["/bin/sh"]
```

<a id="run-builds"></a>

## Memulai pembangunan

[Actions → Bangun image dasar → Jalankan alur kerja](https://github.com/Low-Price-Hosting/Container/actions/workflows/build-base-images.yml):

| Kolom | Penggunaan |
|---|---|
| `distribution` | `all` atau nama distribusi. |
| `version` | `all` atau versi lengkap, seperti `24.04`, `trixie`, `stream10`, atau `rolling`. |
| `verify_only` | `true`: bangun/uji ulang tanpa publikasi. `false`: bangun/uji dan publikasikan image yang berubah atau belum tersedia. |

Semua arsitektur yang ditemukan untuk versi yang dipilih akan diproses. Dengan GitHub CLI:

```bash
# Bangun dan publikasikan image yang berubah atau belum tersedia untuk semua distribusi.
gh workflow run build-base-images.yml \
  --repo Low-Price-Hosting/Container --ref main \
  -f distribution=all -f version=all -f verify_only=false

# Hanya bangun dan uji image Fedora.
gh workflow run build-base-images.yml \
  --repo Low-Price-Hosting/Container --ref main \
  -f distribution=Fedora -f version=all -f verify_only=true
```

Lencana pembangunan di atas menampilkan hasil alur kerja terakhir; proses yang hanya melakukan verifikasi tidak memublikasikan image.

<a id="oci-metadata"></a>

## Tag dan informasi image

| Referensi | Arti |
|---|---|
| `ubuntu:24.04`, `debian:trixie`, `centos:stream10` | Tag multiarsitektur yang memuat arsitektur yang telah diuji untuk versi terkait. |
| `latest` dan alias lainnya | Tag yang ditentukan berdasarkan katalog versi distribusi. |
| `<image>@sha256:<digest>` | Referensi konten image yang tidak dapat diubah. |

Informasi sumber, versi, dan pembangunan image tersedia dalam metadata OCI:

```bash
docker image inspect --format '{{json .Config.Labels}}' \
  ghcr.io/low-price-hosting/ubuntu:latest
```

`org.opencontainers.image.source` menunjukkan repositori resep sumber, `org.opencontainers.image.version` menunjukkan versi, dan `io.low-price-hosting.build.source` menunjukkan kode pembangunan. Indeks multiarsitektur dan anotasi arsitektur dapat dibaca dengan `docker buildx imagetools inspect --raw`.
