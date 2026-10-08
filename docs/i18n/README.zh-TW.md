<div align="center">

**🌐 語言**

[Türkçe](../../README.md) · [English](README.en.md) · [简体中文](README.zh-CN.md) · **繁體中文** · [日本語](README.ja.md) · [한국어](README.ko.md)

[Deutsch](README.de.md) · [Français](README.fr.md) · [Español](README.es.md) · [Português (Brasil)](README.pt-BR.md) · [Italiano](README.it.md) · [Русский](README.ru.md)

[Українська](README.uk.md) · [العربية](README.ar.md) · [فارسی](README.fa.md) · [हिन्दी](README.hi.md) · [Bahasa Indonesia](README.id.md) · [Tiếng Việt](README.vi.md)

</div>

---

# Low-Price-Hosting · Container

**Linux 基礎容器映像 — 依原始碼建置配方產生，按架構測試，並發布至 GHCR。**

[![建置狀態](https://github.com/Low-Price-Hosting/Container/actions/workflows/build-base-images.yml/badge.svg?branch=main)](https://github.com/Low-Price-Hosting/Container/actions/workflows/build-base-images.yml)
[![原始碼更新](https://github.com/Low-Price-Hosting/Cron/actions/workflows/mirror-container-sources.yml/badge.svg?branch=main)](https://github.com/Low-Price-Hosting/Cron/actions/workflows/mirror-container-sources.yml)
[![映像倉庫：GHCR](https://img.shields.io/badge/registry-GHCR-0969da?style=flat-square)](https://github.com/orgs/Low-Price-Hosting/packages?ecosystem=container)

**8 個發行版** · **動態版本與架構** · **建置 → 測試 → 發布**

[映像](#images-and-downloads) · [架構](#versions-and-architectures) · [使用方式](#quick-start) · [啟動建置](#run-builds) · [建置流程](#pipeline) · [映像資訊](#oci-metadata)

---

<a id="images-and-downloads"></a>

## 映像與下載量

| 發行版 | 映像參照 | 標籤與 OS/Arch | 總下載量 |
|---|---|---|---|
| [Ubuntu](https://github.com/Low-Price-Hosting/Ubuntu) | `ghcr.io/low-price-hosting/ubuntu` | [套件](https://github.com/orgs/Low-Price-Hosting/packages/container/package/ubuntu) | [![ubuntu GHCR 下載次數](https://img.shields.io/badge/dynamic/regex?url=https%3A%2F%2Fgithub.com%2Forgs%2FLow-Price-Hosting%2Fpackages%2Fcontainer%2Fpackage%2Fubuntu&search=Total%20downloads%3C%2Fspan%3E%5Cs%2A%3Ch3%20title%3D%22%28%5B0-9%2C%5D%2B%29%22%3E&replace=%241&label=GHCR%20downloads&color=0969da&style=flat-square)](https://github.com/orgs/Low-Price-Hosting/packages/container/package/ubuntu) |
| [Debian](https://github.com/Low-Price-Hosting/Debian) | `ghcr.io/low-price-hosting/debian` | [套件](https://github.com/orgs/Low-Price-Hosting/packages/container/package/debian) | [![debian GHCR 下載次數](https://img.shields.io/badge/dynamic/regex?url=https%3A%2F%2Fgithub.com%2Forgs%2FLow-Price-Hosting%2Fpackages%2Fcontainer%2Fpackage%2Fdebian&search=Total%20downloads%3C%2Fspan%3E%5Cs%2A%3Ch3%20title%3D%22%28%5B0-9%2C%5D%2B%29%22%3E&replace=%241&label=GHCR%20downloads&color=0969da&style=flat-square)](https://github.com/orgs/Low-Price-Hosting/packages/container/package/debian) |
| [CentOS Stream](https://github.com/Low-Price-Hosting/Centos) | `ghcr.io/low-price-hosting/centos` | [套件](https://github.com/orgs/Low-Price-Hosting/packages/container/package/centos) | [![centos GHCR 下載次數](https://img.shields.io/badge/dynamic/regex?url=https%3A%2F%2Fgithub.com%2Forgs%2FLow-Price-Hosting%2Fpackages%2Fcontainer%2Fpackage%2Fcentos&search=Total%20downloads%3C%2Fspan%3E%5Cs%2A%3Ch3%20title%3D%22%28%5B0-9%2C%5D%2B%29%22%3E&replace=%241&label=GHCR%20downloads&color=0969da&style=flat-square)](https://github.com/orgs/Low-Price-Hosting/packages/container/package/centos) |
| [Alpine](https://github.com/Low-Price-Hosting/Alpine) | `ghcr.io/low-price-hosting/alpine` | [套件](https://github.com/orgs/Low-Price-Hosting/packages/container/package/alpine) | [![alpine GHCR 下載次數](https://img.shields.io/badge/dynamic/regex?url=https%3A%2F%2Fgithub.com%2Forgs%2FLow-Price-Hosting%2Fpackages%2Fcontainer%2Fpackage%2Falpine&search=Total%20downloads%3C%2Fspan%3E%5Cs%2A%3Ch3%20title%3D%22%28%5B0-9%2C%5D%2B%29%22%3E&replace=%241&label=GHCR%20downloads&color=0969da&style=flat-square)](https://github.com/orgs/Low-Price-Hosting/packages/container/package/alpine) |
| [Fedora](https://github.com/Low-Price-Hosting/Fedora) | `ghcr.io/low-price-hosting/fedora` | [套件](https://github.com/orgs/Low-Price-Hosting/packages/container/package/fedora) | [![fedora GHCR 下載次數](https://img.shields.io/badge/dynamic/regex?url=https%3A%2F%2Fgithub.com%2Forgs%2FLow-Price-Hosting%2Fpackages%2Fcontainer%2Fpackage%2Ffedora&search=Total%20downloads%3C%2Fspan%3E%5Cs%2A%3Ch3%20title%3D%22%28%5B0-9%2C%5D%2B%29%22%3E&replace=%241&label=GHCR%20downloads&color=0969da&style=flat-square)](https://github.com/orgs/Low-Price-Hosting/packages/container/package/fedora) |
| [AlmaLinux](https://github.com/Low-Price-Hosting/AlmaLinux) | `ghcr.io/low-price-hosting/almalinux` | [套件](https://github.com/orgs/Low-Price-Hosting/packages/container/package/almalinux) | [![almalinux GHCR 下載次數](https://img.shields.io/badge/dynamic/regex?url=https%3A%2F%2Fgithub.com%2Forgs%2FLow-Price-Hosting%2Fpackages%2Fcontainer%2Fpackage%2Falmalinux&search=Total%20downloads%3C%2Fspan%3E%5Cs%2A%3Ch3%20title%3D%22%28%5B0-9%2C%5D%2B%29%22%3E&replace=%241&label=GHCR%20downloads&color=0969da&style=flat-square)](https://github.com/orgs/Low-Price-Hosting/packages/container/package/almalinux) |
| [Arch Linux](https://github.com/Low-Price-Hosting/ArchLinux) | `ghcr.io/low-price-hosting/archlinux` | [套件](https://github.com/orgs/Low-Price-Hosting/packages/container/package/archlinux) | [![archlinux GHCR 下載次數](https://img.shields.io/badge/dynamic/regex?url=https%3A%2F%2Fgithub.com%2Forgs%2FLow-Price-Hosting%2Fpackages%2Fcontainer%2Fpackage%2Farchlinux&search=Total%20downloads%3C%2Fspan%3E%5Cs%2A%3Ch3%20title%3D%22%28%5B0-9%2C%5D%2B%29%22%3E&replace=%241&label=GHCR%20downloads&color=0969da&style=flat-square)](https://github.com/orgs/Low-Price-Hosting/packages/container/package/archlinux) |
| [Rocky Linux](https://github.com/Low-Price-Hosting/RockyLinux) | `ghcr.io/low-price-hosting/rockylinux` | [套件](https://github.com/orgs/Low-Price-Hosting/packages/container/package/rockylinux) | [![rockylinux GHCR 下載次數](https://img.shields.io/badge/dynamic/regex?url=https%3A%2F%2Fgithub.com%2Forgs%2FLow-Price-Hosting%2Fpackages%2Fcontainer%2Fpackage%2Frockylinux&search=Total%20downloads%3C%2Fspan%3E%5Cs%2A%3Ch3%20title%3D%22%28%5B0-9%2C%5D%2B%29%22%3E&replace=%241&label=GHCR%20downloads&color=0969da&style=flat-square)](https://github.com/orgs/Low-Price-Hosting/packages/container/package/rockylinux) |

下載徽章顯示 GitHub Packages 中的 **Total downloads（總下載量）**。各版本的下載量和已發布架構列於對應的套件頁面。快取可能導致計數延遲；無法讀取計數**不代表 0**。

<a id="versions-and-architectures"></a>

## 版本與架構參考

以下版本與架構參考來自 [2026 年 10 月 8 日的探索計畫](https://github.com/Low-Price-Hosting/Container/actions/runs/37741062225)。這些是探索到的目標；請從所選標籤的 **OS/Arch** 欄位或 OCI 索引確認已發布的架構。

| 發行版 | 版本 | 平台 — 含 `linux/` 前綴 |
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

\* 此計畫未將 Rocky Linux 10 的 `riscv64` 目標納入建置。架構集合可能因版本而異。

檢查某個標籤實際包含的架構：

```bash
docker buildx imagetools inspect ghcr.io/low-price-hosting/ubuntu:24.04
docker buildx imagetools inspect --raw ghcr.io/low-price-hosting/ubuntu:24.04
```

<a id="quick-start"></a>

## 快速使用

將範例中的 `24.04` 替換為您想使用的**已發布標籤**。下載公開映像無須登入 GHCR。

### 下載並執行

```bash
docker pull ghcr.io/low-price-hosting/ubuntu:24.04
docker run --rm -it ghcr.io/low-price-hosting/ubuntu:24.04 /bin/sh
```

Docker 會從多架構標籤中選擇符合您電腦架構的映像。

### 選擇架構

```bash
docker pull --platform linux/arm64 ghcr.io/low-price-hosting/ubuntu:24.04

docker run --rm --platform linux/arm64 \
  ghcr.io/low-price-hosting/ubuntu:24.04 \
  /bin/sh -c 'cat /etc/os-release'
```

執行適用於其他處理器系列的映像需要相應的模擬支援。

### 以摘要固定映像

```bash
docker image inspect --format '{{json .RepoDigests}}' \
  ghcr.io/low-price-hosting/ubuntu:24.04

# 將 <digest> 替換為映像的 SHA256 值。
docker pull ghcr.io/low-price-hosting/ubuntu@sha256:<digest>
```

版本標籤可能更新；摘要讓您能再次使用同一個映像。

### 用於您自己的映像

```dockerfile
FROM ghcr.io/low-price-hosting/ubuntu:24.04

COPY app/ /opt/app/
WORKDIR /opt/app
CMD ["/bin/sh"]
```

<a id="run-builds"></a>

## 啟動建置

[動作 → 建置基礎映像 → 執行工作流程](https://github.com/Low-Price-Hosting/Container/actions/workflows/build-base-images.yml)：

| 欄位 | 用法 |
|---|---|
| `distribution` | `all` 或某個發行版名稱。 |
| `version` | `all` 或確切版本，例如 `24.04`、`trixie`、`stream10` 或 `rolling`。 |
| `verify_only` | `true`：重新建置並測試，不發布。`false`：建置、測試並發布有變更或缺少的映像。 |

所選版本的所有已探索架構都會處理。使用 GitHub CLI：

```bash
# 為所有發行版建置並發布有變更或缺少的映像。
gh workflow run build-base-images.yml \
  --repo Low-Price-Hosting/Container --ref main \
  -f distribution=all -f version=all -f verify_only=false

# 僅建置並測試 Fedora 映像。
gh workflow run build-base-images.yml \
  --repo Low-Price-Hosting/Container --ref main \
  -f distribution=Fedora -f version=all -f verify_only=true
```

上方的建置徽章顯示最近一次工作流程的結果；僅驗證的執行不會發布映像。

<a id="pipeline"></a>

## 建置流程

```mermaid
flowchart LR
    D["版本與架構探索"] --> B["建置"]
    B --> T["測試"]
    T --> P["發布"]
    P --> G["GHCR 多架構映像"]
```

| 階段 | 對映像執行的操作 |
|---|---|
| **建置** | 使用發行版的容器產生配方建立 rootfs/映像。 |
| **測試** | 在獨立的執行器上執行映像；檢查發行版識別、套件管理器、架構和原始碼標籤。 |
| **發布** | 某個版本的所有預期架構通過測試後，發布該版本的多架構標籤。 |

每個建置/測試目標使用獨立的執行器。測試屬於基本執行檢查，並非完整的應用程式相容性測試。

新版本與架構會從來源目錄清單中自動探索。相關配方、原始碼分支、引導映像清單及套件倉庫準備就緒後，目標才會加入建置計畫。原始碼透過每小時執行的 Cron 流程更新；GitHub 排程可能延遲。

<a id="oci-metadata"></a>

## 標籤與映像資訊

| 參照 | 意義 |
|---|---|
| `ubuntu:24.04`, `debian:trixie`, `centos:stream10` | 包含對應版本已通過測試架構的多架構標籤。 |
| `latest` 與其他別名 | 依發行版的版本目錄決定的標籤。 |
| `<image>@sha256:<digest>` | 不可變的映像內容參照。 |

映像的原始碼、版本及產生資訊可在 OCI 中繼資料中查看：

```bash
docker image inspect --format '{{json .Config.Labels}}' \
  ghcr.io/low-price-hosting/ubuntu:24.04
```

`org.opencontainers.image.source` 指向原始碼配方倉庫，`org.opencontainers.image.version` 表示版本，`io.low-price-hosting.build.source` 指向產生程式碼。可透過 `docker buildx imagetools inspect --raw` 讀取多架構索引與架構註解。
