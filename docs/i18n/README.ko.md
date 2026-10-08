<div align="center">

**🌐 언어**

[Türkçe](../../README.md) · [English](README.en.md) · [简体中文](README.zh-CN.md) · [繁體中文](README.zh-TW.md) · [日本語](README.ja.md) · **한국어**

[Deutsch](README.de.md) · [Français](README.fr.md) · [Español](README.es.md) · [Português (Brasil)](README.pt-BR.md) · [Italiano](README.it.md) · [Русский](README.ru.md)

[Українська](README.uk.md) · [العربية](README.ar.md) · [فارسی](README.fa.md) · [हिन्दी](README.hi.md) · [Bahasa Indonesia](README.id.md) · [Tiếng Việt](README.vi.md)

</div>

---

# Low-Price-Hosting · Container

**Linux 기본 컨테이너 이미지 — 소스 빌드 레시피로 생성하고, 아키텍처별로 테스트한 뒤 GHCR에 게시합니다.**

[![빌드 상태](https://github.com/Low-Price-Hosting/Container/actions/workflows/build-base-images.yml/badge.svg?branch=main)](https://github.com/Low-Price-Hosting/Container/actions/workflows/build-base-images.yml)
[![소스 업데이트](https://github.com/Low-Price-Hosting/Cron/actions/workflows/mirror-container-sources.yml/badge.svg?branch=main)](https://github.com/Low-Price-Hosting/Cron/actions/workflows/mirror-container-sources.yml)
[![레지스트리: GHCR](https://img.shields.io/badge/registry-GHCR-0969da?style=flat-square)](https://github.com/orgs/Low-Price-Hosting/packages?ecosystem=container)

**8개 배포판** · **동적으로 확인하는 버전과 아키텍처** · **빌드 → 테스트 → 게시**

[이미지](#images-and-downloads) · [아키텍처](#versions-and-architectures) · [사용법](#quick-start) · [빌드 시작](#run-builds) · [빌드 흐름](#pipeline) · [이미지 정보](#oci-metadata)

---

<a id="images-and-downloads"></a>

## 이미지와 다운로드 수

| 배포판 | 이미지 참조 | 태그와 OS/Arch | 총 다운로드 수 |
|---|---|---|---|
| [Ubuntu](https://github.com/Low-Price-Hosting/Ubuntu) | `ghcr.io/low-price-hosting/ubuntu` | [패키지](https://github.com/orgs/Low-Price-Hosting/packages/container/package/ubuntu) | [![ubuntu GHCR 다운로드 수](https://img.shields.io/badge/dynamic/regex?url=https%3A%2F%2Fgithub.com%2Forgs%2FLow-Price-Hosting%2Fpackages%2Fcontainer%2Fpackage%2Fubuntu&search=Total%20downloads%3C%2Fspan%3E%5Cs%2A%3Ch3%20title%3D%22%28%5B0-9%2C%5D%2B%29%22%3E&replace=%241&label=GHCR%20downloads&color=0969da&style=flat-square)](https://github.com/orgs/Low-Price-Hosting/packages/container/package/ubuntu) |
| [Debian](https://github.com/Low-Price-Hosting/Debian) | `ghcr.io/low-price-hosting/debian` | [패키지](https://github.com/orgs/Low-Price-Hosting/packages/container/package/debian) | [![debian GHCR 다운로드 수](https://img.shields.io/badge/dynamic/regex?url=https%3A%2F%2Fgithub.com%2Forgs%2FLow-Price-Hosting%2Fpackages%2Fcontainer%2Fpackage%2Fdebian&search=Total%20downloads%3C%2Fspan%3E%5Cs%2A%3Ch3%20title%3D%22%28%5B0-9%2C%5D%2B%29%22%3E&replace=%241&label=GHCR%20downloads&color=0969da&style=flat-square)](https://github.com/orgs/Low-Price-Hosting/packages/container/package/debian) |
| [CentOS Stream](https://github.com/Low-Price-Hosting/Centos) | `ghcr.io/low-price-hosting/centos` | [패키지](https://github.com/orgs/Low-Price-Hosting/packages/container/package/centos) | [![centos GHCR 다운로드 수](https://img.shields.io/badge/dynamic/regex?url=https%3A%2F%2Fgithub.com%2Forgs%2FLow-Price-Hosting%2Fpackages%2Fcontainer%2Fpackage%2Fcentos&search=Total%20downloads%3C%2Fspan%3E%5Cs%2A%3Ch3%20title%3D%22%28%5B0-9%2C%5D%2B%29%22%3E&replace=%241&label=GHCR%20downloads&color=0969da&style=flat-square)](https://github.com/orgs/Low-Price-Hosting/packages/container/package/centos) |
| [Alpine](https://github.com/Low-Price-Hosting/Alpine) | `ghcr.io/low-price-hosting/alpine` | [패키지](https://github.com/orgs/Low-Price-Hosting/packages/container/package/alpine) | [![alpine GHCR 다운로드 수](https://img.shields.io/badge/dynamic/regex?url=https%3A%2F%2Fgithub.com%2Forgs%2FLow-Price-Hosting%2Fpackages%2Fcontainer%2Fpackage%2Falpine&search=Total%20downloads%3C%2Fspan%3E%5Cs%2A%3Ch3%20title%3D%22%28%5B0-9%2C%5D%2B%29%22%3E&replace=%241&label=GHCR%20downloads&color=0969da&style=flat-square)](https://github.com/orgs/Low-Price-Hosting/packages/container/package/alpine) |
| [Fedora](https://github.com/Low-Price-Hosting/Fedora) | `ghcr.io/low-price-hosting/fedora` | [패키지](https://github.com/orgs/Low-Price-Hosting/packages/container/package/fedora) | [![fedora GHCR 다운로드 수](https://img.shields.io/badge/dynamic/regex?url=https%3A%2F%2Fgithub.com%2Forgs%2FLow-Price-Hosting%2Fpackages%2Fcontainer%2Fpackage%2Ffedora&search=Total%20downloads%3C%2Fspan%3E%5Cs%2A%3Ch3%20title%3D%22%28%5B0-9%2C%5D%2B%29%22%3E&replace=%241&label=GHCR%20downloads&color=0969da&style=flat-square)](https://github.com/orgs/Low-Price-Hosting/packages/container/package/fedora) |
| [AlmaLinux](https://github.com/Low-Price-Hosting/AlmaLinux) | `ghcr.io/low-price-hosting/almalinux` | [패키지](https://github.com/orgs/Low-Price-Hosting/packages/container/package/almalinux) | [![almalinux GHCR 다운로드 수](https://img.shields.io/badge/dynamic/regex?url=https%3A%2F%2Fgithub.com%2Forgs%2FLow-Price-Hosting%2Fpackages%2Fcontainer%2Fpackage%2Falmalinux&search=Total%20downloads%3C%2Fspan%3E%5Cs%2A%3Ch3%20title%3D%22%28%5B0-9%2C%5D%2B%29%22%3E&replace=%241&label=GHCR%20downloads&color=0969da&style=flat-square)](https://github.com/orgs/Low-Price-Hosting/packages/container/package/almalinux) |
| [Arch Linux](https://github.com/Low-Price-Hosting/ArchLinux) | `ghcr.io/low-price-hosting/archlinux` | [패키지](https://github.com/orgs/Low-Price-Hosting/packages/container/package/archlinux) | [![archlinux GHCR 다운로드 수](https://img.shields.io/badge/dynamic/regex?url=https%3A%2F%2Fgithub.com%2Forgs%2FLow-Price-Hosting%2Fpackages%2Fcontainer%2Fpackage%2Farchlinux&search=Total%20downloads%3C%2Fspan%3E%5Cs%2A%3Ch3%20title%3D%22%28%5B0-9%2C%5D%2B%29%22%3E&replace=%241&label=GHCR%20downloads&color=0969da&style=flat-square)](https://github.com/orgs/Low-Price-Hosting/packages/container/package/archlinux) |
| [Rocky Linux](https://github.com/Low-Price-Hosting/RockyLinux) | `ghcr.io/low-price-hosting/rockylinux` | [패키지](https://github.com/orgs/Low-Price-Hosting/packages/container/package/rockylinux) | [![rockylinux GHCR 다운로드 수](https://img.shields.io/badge/dynamic/regex?url=https%3A%2F%2Fgithub.com%2Forgs%2FLow-Price-Hosting%2Fpackages%2Fcontainer%2Fpackage%2Frockylinux&search=Total%20downloads%3C%2Fspan%3E%5Cs%2A%3Ch3%20title%3D%22%28%5B0-9%2C%5D%2B%29%22%3E&replace=%241&label=GHCR%20downloads&color=0969da&style=flat-square)](https://github.com/orgs/Low-Price-Hosting/packages/container/package/rockylinux) |

다운로드 배지는 GitHub Packages의 **Total downloads(총 다운로드 수)** 값을 표시합니다. 버전별 다운로드 수와 게시된 아키텍처는 해당 패키지 페이지에서 확인할 수 있습니다. 캐시로 인해 카운터 갱신이 지연될 수 있으며, 읽을 수 없는 카운터는 **0을 뜻하지 않습니다**.

<a id="versions-and-architectures"></a>

## 버전과 아키텍처 참고 정보

[2026년 10월 8일 탐색 계획](https://github.com/Low-Price-Hosting/Container/actions/runs/37741062225)의 버전 및 아키텍처 참고 정보입니다. 이는 탐색된 대상입니다. 게시된 아키텍처는 선택한 태그의 **OS/Arch** 필드나 OCI 인덱스에서 확인하세요.

| 배포판 | 버전 | 플랫폼 — `linux/` 접두사 포함 |
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
| Rocky Linux | `10` | `amd64`, `arm64`, `ppc64le`, `riscv64`*, `s390x` |

\* 이 계획에서 Rocky Linux 10의 `riscv64` 대상은 빌드에서 제외되었습니다. 아키텍처 구성은 버전에 따라 달라질 수 있습니다.

태그에 실제로 포함된 아키텍처를 확인하세요:

```bash
docker buildx imagetools inspect ghcr.io/low-price-hosting/ubuntu:24.04
docker buildx imagetools inspect --raw ghcr.io/low-price-hosting/ubuntu:24.04
```

<a id="quick-start"></a>

## 빠른 시작

예제의 `24.04`를 사용하려는 **게시된 태그**로 바꾸세요. 공개 이미지를 다운로드할 때는 GHCR 로그인이 필요하지 않습니다.

### 다운로드하고 실행하기

```bash
docker pull ghcr.io/low-price-hosting/ubuntu:24.04
docker run --rm -it ghcr.io/low-price-hosting/ubuntu:24.04 /bin/sh
```

Docker는 다중 아키텍처 태그에서 컴퓨터의 아키텍처에 맞는 이미지를 선택합니다.

### 아키텍처 선택하기

```bash
docker pull --platform linux/arm64 ghcr.io/low-price-hosting/ubuntu:24.04

docker run --rm --platform linux/arm64 \
  ghcr.io/low-price-hosting/ubuntu:24.04 \
  /bin/sh -c 'cat /etc/os-release'
```

다른 프로세서 계열용 이미지를 실행하려면 적절한 에뮬레이션이 필요합니다.

### 다이제스트로 고정하기

```bash
docker image inspect --format '{{json .RepoDigests}}' \
  ghcr.io/low-price-hosting/ubuntu:24.04

# <digest>를 이미지의 SHA256 값으로 바꾸세요.
docker pull ghcr.io/low-price-hosting/ubuntu@sha256:<digest>
```

버전 태그는 갱신될 수 있습니다. 다이제스트를 사용하면 같은 이미지를 다시 사용할 수 있습니다.

### 자신의 이미지에서 사용하기

```dockerfile
FROM ghcr.io/low-price-hosting/ubuntu:24.04

COPY app/ /opt/app/
WORKDIR /opt/app
CMD ["/bin/sh"]
```

<a id="run-builds"></a>

## 빌드 시작

[작업 → 기본 이미지 빌드 → 워크플로 실행](https://github.com/Low-Price-Hosting/Container/actions/workflows/build-base-images.yml):

| 필드 | 사용법 |
|---|---|
| `distribution` | `all` 또는 배포판 이름. |
| `version` | `all` 또는 `24.04`, `trixie`, `stream10`, `rolling` 등의 정확한 버전. |
| `verify_only` | `true`: 다시 빌드하고 테스트하며 게시하지 않습니다. `false`: 변경되었거나 누락된 이미지를 빌드하고 테스트한 뒤 게시합니다. |

선택한 버전에서 탐색된 모든 아키텍처를 처리합니다. GitHub CLI 사용 시:

```bash
# 모든 배포판에서 변경되었거나 누락된 이미지를 빌드하고 게시합니다.
gh workflow run build-base-images.yml \
  --repo Low-Price-Hosting/Container --ref main \
  -f distribution=all -f version=all -f verify_only=false

# Fedora 이미지를 빌드하고 테스트만 합니다.
gh workflow run build-base-images.yml \
  --repo Low-Price-Hosting/Container --ref main \
  -f distribution=Fedora -f version=all -f verify_only=true
```

위의 빌드 배지는 최근 워크플로 결과를 표시합니다. 검증만 수행한 실행은 이미지를 게시하지 않습니다.

<a id="pipeline"></a>

## 빌드 흐름

```mermaid
flowchart LR
    D["버전과 아키텍처 탐색"] --> B["빌드"]
    B --> T["테스트"]
    T --> P["게시"]
    P --> G["GHCR 다중 아키텍처 이미지"]
```

| 단계 | 이미지에 수행하는 작업 |
|---|---|
| **빌드** | 배포판의 컨테이너 생성 레시피로 rootfs/이미지를 만듭니다. |
| **테스트** | 별도의 러너에서 이미지를 실행하고 배포판 ID, 패키지 관리자, 아키텍처, 소스 레이블을 확인합니다. |
| **게시** | 해당 버전의 예상 아키텍처가 모두 테스트를 통과하면 다중 아키텍처 버전 태그를 게시합니다. |

각 빌드/테스트 대상은 별도의 러너를 사용합니다. 테스트는 기본 동작 확인이며 포괄적인 애플리케이션 호환성 테스트가 아닙니다.

새 버전과 아키텍처는 소스 카탈로그에서 자동으로 탐색합니다. 관련 레시피, 소스 브랜치, 부트스트랩 매니페스트, 패키지 저장소가 준비되면 빌드 계획에 포함합니다. 소스는 매시간 실행되는 Cron 흐름을 통해 갱신되며 GitHub 예약 실행은 지연될 수 있습니다.

<a id="oci-metadata"></a>

## 태그와 이미지 정보

| 참조 | 의미 |
|---|---|
| `ubuntu:24.04`, `debian:trixie`, `centos:stream10` | 해당 버전의 테스트된 아키텍처를 포함하는 다중 아키텍처 태그. |
| `latest` 및 기타 별칭 | 배포판의 버전 카탈로그에 따라 정해지는 태그. |
| `<image>@sha256:<digest>` | 변경되지 않는 이미지 내용 참조. |

이미지의 소스, 버전, 생성 정보는 OCI 메타데이터에서 확인할 수 있습니다:

```bash
docker image inspect --format '{{json .Config.Labels}}' \
  ghcr.io/low-price-hosting/ubuntu:24.04
```

`org.opencontainers.image.source`는 소스 레시피 저장소를, `org.opencontainers.image.version`은 버전을, `io.low-price-hosting.build.source`는 생성 코드를 나타냅니다. 다중 아키텍처 인덱스와 아키텍처 주석은 `docker buildx imagetools inspect --raw`로 읽을 수 있습니다.
