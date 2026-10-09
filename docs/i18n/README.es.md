<div align="center">

**🌐 Idiomas**

[Türkçe](../../README.md) · [English](README.en.md) · [简体中文](README.zh-CN.md) · [繁體中文](README.zh-TW.md) · [日本語](README.ja.md) · [한국어](README.ko.md)

[Deutsch](README.de.md) · [Français](README.fr.md) · **Español** · [Português (Brasil)](README.pt-BR.md) · [Italiano](README.it.md) · [Русский](README.ru.md)

[Українська](README.uk.md) · [العربية](README.ar.md) · [فارسی](README.fa.md) · [हिन्दी](README.hi.md) · [Bahasa Indonesia](README.id.md) · [Tiếng Việt](README.vi.md)

</div>

---

# Low-Price-Hosting · Container

**Imágenes base de Linux para contenedores — compilación a partir de recetas fuente, pruebas por arquitectura y publicación en GHCR, Docker Hub y Quay.**

[![Estado de compilación](https://github.com/Low-Price-Hosting/Container/actions/workflows/build-base-images.yml/badge.svg?branch=main)](https://github.com/Low-Price-Hosting/Container/actions/workflows/build-base-images.yml)
[![Actualizaciones de las fuentes](https://github.com/Low-Price-Hosting/Cron/actions/workflows/mirror-container-sources.yml/badge.svg?branch=main)](https://github.com/Low-Price-Hosting/Cron/actions/workflows/mirror-container-sources.yml)
[![Registro: GHCR](https://img.shields.io/badge/registry-GHCR-0969da?style=flat-square)](https://github.com/orgs/Low-Price-Hosting/packages?ecosystem=container)
[![Registro: Docker Hub](https://img.shields.io/badge/registry-Docker_Hub-2496ed?style=flat-square)](https://hub.docker.com/u/lphllc)
[![Registro: Quay](https://img.shields.io/badge/registry-Quay-ee0000?style=flat-square)](https://quay.io/organization/lowpricehosting)

**8 distribuciones** · **Versiones y arquitecturas dinámicas** · **Compilar → Probar → Publicar**

[Imágenes](#images-and-downloads) · [Arquitecturas](#versions-and-architectures) · [Uso](#quick-start) · [Iniciar compilaciones](#run-builds) · [Información de las imágenes](#oci-metadata)

---

<a id="images-and-downloads"></a>

## Imágenes y descargas

| Distribución | GHCR | Docker Hub | Quay |
|---|---|---|---|
| [Ubuntu](https://github.com/Low-Price-Hosting/Ubuntu) | [![ubuntu número de descargas de GHCR](https://img.shields.io/badge/dynamic/regex?url=https%3A%2F%2Fgithub.com%2Forgs%2FLow-Price-Hosting%2Fpackages%2Fcontainer%2Fpackage%2Fubuntu&search=Total%20downloads%3C%2Fspan%3E%5Cs%2A%3Ch3%20title%3D%22%28%5B0-9%2C%5D%2B%29%22%3E&replace=%241&label=GHCR%20downloads&color=0969da&style=flat-square&cacheSeconds=300)](https://github.com/orgs/Low-Price-Hosting/packages/container/package/ubuntu) | [![ubuntu Docker Hub pulls](https://img.shields.io/docker/pulls/lphllc/ubuntu?label=Docker%20pulls&style=flat-square)](https://hub.docker.com/r/lphllc/ubuntu) | [![ubuntu Quay architectures](https://img.shields.io/badge/dynamic/json?url=https%3A%2F%2Fquay.io%2Fapi%2Fv1%2Frepository%2Flowpricehosting%2Fubuntu%2Ftag%2F%3FspecificTag%3Dlatest%26onlyActiveTags%3Dtrue&query=%24.tags%5B0%5D.child_manifest_count&label=Quay%20architectures&color=ee0000&style=flat-square&cacheSeconds=300)](https://quay.io/repository/lowpricehosting/ubuntu?tab=tags) |
| [Debian](https://github.com/Low-Price-Hosting/Debian) | [![debian número de descargas de GHCR](https://img.shields.io/badge/dynamic/regex?url=https%3A%2F%2Fgithub.com%2Forgs%2FLow-Price-Hosting%2Fpackages%2Fcontainer%2Fpackage%2Fdebian&search=Total%20downloads%3C%2Fspan%3E%5Cs%2A%3Ch3%20title%3D%22%28%5B0-9%2C%5D%2B%29%22%3E&replace=%241&label=GHCR%20downloads&color=0969da&style=flat-square&cacheSeconds=300)](https://github.com/orgs/Low-Price-Hosting/packages/container/package/debian) | [![debian Docker Hub pulls](https://img.shields.io/docker/pulls/lphllc/debian?label=Docker%20pulls&style=flat-square)](https://hub.docker.com/r/lphllc/debian) | [![debian Quay architectures](https://img.shields.io/badge/dynamic/json?url=https%3A%2F%2Fquay.io%2Fapi%2Fv1%2Frepository%2Flowpricehosting%2Fdebian%2Ftag%2F%3FspecificTag%3Dlatest%26onlyActiveTags%3Dtrue&query=%24.tags%5B0%5D.child_manifest_count&label=Quay%20architectures&color=ee0000&style=flat-square&cacheSeconds=300)](https://quay.io/repository/lowpricehosting/debian?tab=tags) |
| [CentOS Stream](https://github.com/Low-Price-Hosting/Centos) | [![centos número de descargas de GHCR](https://img.shields.io/badge/dynamic/regex?url=https%3A%2F%2Fgithub.com%2Forgs%2FLow-Price-Hosting%2Fpackages%2Fcontainer%2Fpackage%2Fcentos&search=Total%20downloads%3C%2Fspan%3E%5Cs%2A%3Ch3%20title%3D%22%28%5B0-9%2C%5D%2B%29%22%3E&replace=%241&label=GHCR%20downloads&color=0969da&style=flat-square&cacheSeconds=300)](https://github.com/orgs/Low-Price-Hosting/packages/container/package/centos) | [![centos Docker Hub pulls](https://img.shields.io/docker/pulls/lphllc/centos?label=Docker%20pulls&style=flat-square)](https://hub.docker.com/r/lphllc/centos) | [![centos Quay architectures](https://img.shields.io/badge/dynamic/json?url=https%3A%2F%2Fquay.io%2Fapi%2Fv1%2Frepository%2Flowpricehosting%2Fcentos%2Ftag%2F%3FspecificTag%3Dlatest%26onlyActiveTags%3Dtrue&query=%24.tags%5B0%5D.child_manifest_count&label=Quay%20architectures&color=ee0000&style=flat-square&cacheSeconds=300)](https://quay.io/repository/lowpricehosting/centos?tab=tags) |
| [Alpine](https://github.com/Low-Price-Hosting/Alpine) | [![alpine número de descargas de GHCR](https://img.shields.io/badge/dynamic/regex?url=https%3A%2F%2Fgithub.com%2Forgs%2FLow-Price-Hosting%2Fpackages%2Fcontainer%2Fpackage%2Falpine&search=Total%20downloads%3C%2Fspan%3E%5Cs%2A%3Ch3%20title%3D%22%28%5B0-9%2C%5D%2B%29%22%3E&replace=%241&label=GHCR%20downloads&color=0969da&style=flat-square&cacheSeconds=300)](https://github.com/orgs/Low-Price-Hosting/packages/container/package/alpine) | [![alpine Docker Hub pulls](https://img.shields.io/docker/pulls/lphllc/alpine?label=Docker%20pulls&style=flat-square)](https://hub.docker.com/r/lphllc/alpine) | [![alpine Quay architectures](https://img.shields.io/badge/dynamic/json?url=https%3A%2F%2Fquay.io%2Fapi%2Fv1%2Frepository%2Flowpricehosting%2Falpine%2Ftag%2F%3FspecificTag%3Dlatest%26onlyActiveTags%3Dtrue&query=%24.tags%5B0%5D.child_manifest_count&label=Quay%20architectures&color=ee0000&style=flat-square&cacheSeconds=300)](https://quay.io/repository/lowpricehosting/alpine?tab=tags) |
| [Fedora](https://github.com/Low-Price-Hosting/Fedora) | [![fedora número de descargas de GHCR](https://img.shields.io/badge/dynamic/regex?url=https%3A%2F%2Fgithub.com%2Forgs%2FLow-Price-Hosting%2Fpackages%2Fcontainer%2Fpackage%2Ffedora&search=Total%20downloads%3C%2Fspan%3E%5Cs%2A%3Ch3%20title%3D%22%28%5B0-9%2C%5D%2B%29%22%3E&replace=%241&label=GHCR%20downloads&color=0969da&style=flat-square&cacheSeconds=300)](https://github.com/orgs/Low-Price-Hosting/packages/container/package/fedora) | [![fedora Docker Hub pulls](https://img.shields.io/docker/pulls/lphllc/fedora?label=Docker%20pulls&style=flat-square)](https://hub.docker.com/r/lphllc/fedora) | [![fedora Quay architectures](https://img.shields.io/badge/dynamic/json?url=https%3A%2F%2Fquay.io%2Fapi%2Fv1%2Frepository%2Flowpricehosting%2Ffedora%2Ftag%2F%3FspecificTag%3Dlatest%26onlyActiveTags%3Dtrue&query=%24.tags%5B0%5D.child_manifest_count&label=Quay%20architectures&color=ee0000&style=flat-square&cacheSeconds=300)](https://quay.io/repository/lowpricehosting/fedora?tab=tags) |
| [AlmaLinux](https://github.com/Low-Price-Hosting/AlmaLinux) | [![almalinux número de descargas de GHCR](https://img.shields.io/badge/dynamic/regex?url=https%3A%2F%2Fgithub.com%2Forgs%2FLow-Price-Hosting%2Fpackages%2Fcontainer%2Fpackage%2Falmalinux&search=Total%20downloads%3C%2Fspan%3E%5Cs%2A%3Ch3%20title%3D%22%28%5B0-9%2C%5D%2B%29%22%3E&replace=%241&label=GHCR%20downloads&color=0969da&style=flat-square&cacheSeconds=300)](https://github.com/orgs/Low-Price-Hosting/packages/container/package/almalinux) | [![almalinux Docker Hub pulls](https://img.shields.io/docker/pulls/lphllc/almalinux?label=Docker%20pulls&style=flat-square)](https://hub.docker.com/r/lphllc/almalinux) | [![almalinux Quay architectures](https://img.shields.io/badge/dynamic/json?url=https%3A%2F%2Fquay.io%2Fapi%2Fv1%2Frepository%2Flowpricehosting%2Falmalinux%2Ftag%2F%3FspecificTag%3Dlatest%26onlyActiveTags%3Dtrue&query=%24.tags%5B0%5D.child_manifest_count&label=Quay%20architectures&color=ee0000&style=flat-square&cacheSeconds=300)](https://quay.io/repository/lowpricehosting/almalinux?tab=tags) |
| [Arch Linux](https://github.com/Low-Price-Hosting/ArchLinux) | [![archlinux número de descargas de GHCR](https://img.shields.io/badge/dynamic/regex?url=https%3A%2F%2Fgithub.com%2Forgs%2FLow-Price-Hosting%2Fpackages%2Fcontainer%2Fpackage%2Farchlinux&search=Total%20downloads%3C%2Fspan%3E%5Cs%2A%3Ch3%20title%3D%22%28%5B0-9%2C%5D%2B%29%22%3E&replace=%241&label=GHCR%20downloads&color=0969da&style=flat-square&cacheSeconds=300)](https://github.com/orgs/Low-Price-Hosting/packages/container/package/archlinux) | [![archlinux Docker Hub pulls](https://img.shields.io/docker/pulls/lphllc/archlinux?label=Docker%20pulls&style=flat-square)](https://hub.docker.com/r/lphllc/archlinux) | [![archlinux Quay architectures](https://img.shields.io/badge/dynamic/json?url=https%3A%2F%2Fquay.io%2Fapi%2Fv1%2Frepository%2Flowpricehosting%2Farchlinux%2Ftag%2F%3FspecificTag%3Dlatest%26onlyActiveTags%3Dtrue&query=%24.tags%5B0%5D.child_manifest_count&label=Quay%20architectures&color=ee0000&style=flat-square&cacheSeconds=300)](https://quay.io/repository/lowpricehosting/archlinux?tab=tags) |
| [Rocky Linux](https://github.com/Low-Price-Hosting/RockyLinux) | [![rockylinux número de descargas de GHCR](https://img.shields.io/badge/dynamic/regex?url=https%3A%2F%2Fgithub.com%2Forgs%2FLow-Price-Hosting%2Fpackages%2Fcontainer%2Fpackage%2Frockylinux&search=Total%20downloads%3C%2Fspan%3E%5Cs%2A%3Ch3%20title%3D%22%28%5B0-9%2C%5D%2B%29%22%3E&replace=%241&label=GHCR%20downloads&color=0969da&style=flat-square&cacheSeconds=300)](https://github.com/orgs/Low-Price-Hosting/packages/container/package/rockylinux) | [![rockylinux Docker Hub pulls](https://img.shields.io/docker/pulls/lphllc/rockylinux?label=Docker%20pulls&style=flat-square)](https://hub.docker.com/r/lphllc/rockylinux) | [![rockylinux Quay architectures](https://img.shields.io/badge/dynamic/json?url=https%3A%2F%2Fquay.io%2Fapi%2Fv1%2Frepository%2Flowpricehosting%2Frockylinux%2Ftag%2F%3FspecificTag%3Dlatest%26onlyActiveTags%3Dtrue&query=%24.tags%5B0%5D.child_manifest_count&label=Quay%20architectures&color=ee0000&style=flat-square&cacheSeconds=300)](https://quay.io/repository/lowpricehosting/rockylinux?tab=tags) |

Los indicadores de GHCR y Docker Hub muestran las descargas totales; el de Quay muestra el número de arquitecturas de la etiqueta `latest`. Haga clic en ellos para consultar las etiquetas y arquitecturas. Los contadores son específicos de cada registro; la caché puede retrasar las actualizaciones.

```bash
docker pull ghcr.io/low-price-hosting/ubuntu:latest
docker pull docker.io/lphllc/ubuntu:latest
docker pull quay.io/lowpricehosting/ubuntu:latest
```

<a id="versions-and-architectures"></a>

## Referencias de versiones y arquitecturas

Referencias de versiones y arquitecturas del [plan de descubrimiento del 8 de octubre de 2026](https://github.com/Low-Price-Hosting/Container/actions/runs/37741062225). Son objetivos descubiertos; compruebe las arquitecturas publicadas en el campo **OS/Arch** de la etiqueta elegida o en su índice OCI.

| Distribución | Versiones | Plataformas — con el prefijo `linux/` |
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

El conjunto de arquitecturas puede variar según la versión.

Examine las arquitecturas reales de una etiqueta:

```bash
docker buildx imagetools inspect ghcr.io/low-price-hosting/ubuntu:latest
docker buildx imagetools inspect --raw ghcr.io/low-price-hosting/ubuntu:latest
```

<a id="quick-start"></a>

## Inicio rápido

Sustituya `latest` en los ejemplos por la **etiqueta publicada** que quiera utilizar. No hace falta iniciar sesión en GHCR para descargar imágenes públicas.

### Descargar y ejecutar

```bash
docker pull ghcr.io/low-price-hosting/ubuntu:latest
docker run --rm -it ghcr.io/low-price-hosting/ubuntu:latest /bin/sh
```

Docker selecciona de la etiqueta multiarquitectura la imagen adecuada para la arquitectura de su equipo.

### Seleccionar una arquitectura

```bash
docker pull --platform linux/arm64 ghcr.io/low-price-hosting/ubuntu:latest

docker run --rm --platform linux/arm64 \
  ghcr.io/low-price-hosting/ubuntu:latest \
  /bin/sh -c 'cat /etc/os-release'
```

Para ejecutar una imagen de otra familia de procesadores se necesita una emulación adecuada.

### Fijar mediante digest

```bash
docker image inspect --format '{{json .RepoDigests}}' \
  ghcr.io/low-price-hosting/ubuntu:latest

# Sustituya <digest> por el valor SHA256 de la imagen.
docker pull ghcr.io/low-price-hosting/ubuntu@sha256:<digest>
```

Las etiquetas de versión pueden actualizarse; el digest permite volver a utilizar la misma imagen.

### Usar en su propia imagen

```dockerfile
FROM ghcr.io/low-price-hosting/ubuntu:latest

COPY app/ /opt/app/
WORKDIR /opt/app
CMD ["/bin/sh"]
```

<a id="run-builds"></a>

## Iniciar compilaciones

[Actions → Compilar imágenes base → Ejecutar flujo de trabajo](https://github.com/Low-Price-Hosting/Container/actions/workflows/build-base-images.yml):

| Campo | Uso |
|---|---|
| `distribution` | `all` o el nombre de una distribución. |
| `version` | `all` o una versión exacta, como `24.04`, `trixie`, `stream10` o `rolling`. |
| `verify_only` | `true`: volver a compilar/probar sin publicar. `false`: compilar/probar y publicar las imágenes modificadas o faltantes. |

Se procesan todas las arquitecturas descubiertas de la versión seleccionada. Con GitHub CLI:

```bash
# Compilar y publicar las imágenes modificadas o faltantes de todas las distribuciones.
gh workflow run build-base-images.yml \
  --repo Low-Price-Hosting/Container --ref main \
  -f distribution=all -f version=all -f verify_only=false

# Solo compilar y probar las imágenes de Fedora.
gh workflow run build-base-images.yml \
  --repo Low-Price-Hosting/Container --ref main \
  -f distribution=Fedora -f version=all -f verify_only=true
```

El indicador de compilación de arriba muestra el resultado del último flujo de trabajo; una ejecución dedicada únicamente a la verificación no publica imágenes.

<a id="oci-metadata"></a>

## Etiquetas e información de las imágenes

| Referencia | Significado |
|---|---|
| `ubuntu:24.04`, `debian:trixie`, `centos:stream10` | Etiqueta multiarquitectura que contiene las arquitecturas probadas de la versión correspondiente. |
| `latest` y otros alias | Etiquetas determinadas según el catálogo de versiones de la distribución. |
| `<image>@sha256:<digest>` | Referencia inmutable al contenido de la imagen. |

La información de origen, versión y construcción de la imagen está en sus metadatos OCI:

```bash
docker image inspect --format '{{json .Config.Labels}}' \
  ghcr.io/low-price-hosting/ubuntu:latest
```

`org.opencontainers.image.source` indica el repositorio de la receta fuente, `org.opencontainers.image.version` la versión e `io.low-price-hosting.build.source` el código de construcción. El índice multiarquitectura y las anotaciones de arquitectura se pueden consultar con `docker buildx imagetools inspect --raw`.
