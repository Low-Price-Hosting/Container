<div align="center">

**🌐 语言**

[Türkçe](../../README.md) · [English](README.en.md) · **简体中文** · [繁體中文](README.zh-TW.md) · [日本語](README.ja.md) · [한국어](README.ko.md)

[Deutsch](README.de.md) · [Français](README.fr.md) · [Español](README.es.md) · [Português (Brasil)](README.pt-BR.md) · [Italiano](README.it.md) · [Русский](README.ru.md)

[Українська](README.uk.md) · [العربية](README.ar.md) · [فارسی](README.fa.md) · [हिन्दी](README.hi.md) · [Bahasa Indonesia](README.id.md) · [Tiếng Việt](README.vi.md)

</div>

---

# Low-Price-Hosting · Container

**Linux 基础容器镜像 — 根据源码构建配方生成，按架构测试，并发布到 GHCR。**

[![构建状态](https://github.com/Low-Price-Hosting/Container/actions/workflows/build-base-images.yml/badge.svg?branch=main)](https://github.com/Low-Price-Hosting/Container/actions/workflows/build-base-images.yml)
[![源码更新](https://github.com/Low-Price-Hosting/Cron/actions/workflows/mirror-container-sources.yml/badge.svg?branch=main)](https://github.com/Low-Price-Hosting/Cron/actions/workflows/mirror-container-sources.yml)
[![镜像仓库：GHCR](https://img.shields.io/badge/registry-GHCR-0969da?style=flat-square)](https://github.com/orgs/Low-Price-Hosting/packages?ecosystem=container)

**8 个发行版** · **动态版本和架构** · **构建 → 测试 → 发布**

[镜像](#images-and-downloads) · [架构](#versions-and-architectures) · [使用](#quick-start) · [启动构建](#run-builds) · [构建流程](#pipeline) · [镜像信息](#oci-metadata)

---

<a id="images-and-downloads"></a>

## 镜像和下载量

| 发行版 | 镜像引用 | 标签和 OS/Arch | 总下载量 |
|---|---|---|---|
| [Ubuntu](https://github.com/Low-Price-Hosting/Ubuntu) | `ghcr.io/low-price-hosting/ubuntu` | [软件包](https://github.com/orgs/Low-Price-Hosting/packages/container/package/ubuntu) | [![ubuntu GHCR 下载次数](https://img.shields.io/badge/dynamic/regex?url=https%3A%2F%2Fgithub.com%2Forgs%2FLow-Price-Hosting%2Fpackages%2Fcontainer%2Fpackage%2Fubuntu&search=Total%20downloads%3C%2Fspan%3E%5Cs%2A%3Ch3%20title%3D%22%28%5B0-9%2C%5D%2B%29%22%3E&replace=%241&label=GHCR%20downloads&color=0969da&style=flat-square)](https://github.com/orgs/Low-Price-Hosting/packages/container/package/ubuntu) |
| [Debian](https://github.com/Low-Price-Hosting/Debian) | `ghcr.io/low-price-hosting/debian` | [软件包](https://github.com/orgs/Low-Price-Hosting/packages/container/package/debian) | [![debian GHCR 下载次数](https://img.shields.io/badge/dynamic/regex?url=https%3A%2F%2Fgithub.com%2Forgs%2FLow-Price-Hosting%2Fpackages%2Fcontainer%2Fpackage%2Fdebian&search=Total%20downloads%3C%2Fspan%3E%5Cs%2A%3Ch3%20title%3D%22%28%5B0-9%2C%5D%2B%29%22%3E&replace=%241&label=GHCR%20downloads&color=0969da&style=flat-square)](https://github.com/orgs/Low-Price-Hosting/packages/container/package/debian) |
| [CentOS Stream](https://github.com/Low-Price-Hosting/Centos) | `ghcr.io/low-price-hosting/centos` | [软件包](https://github.com/orgs/Low-Price-Hosting/packages/container/package/centos) | [![centos GHCR 下载次数](https://img.shields.io/badge/dynamic/regex?url=https%3A%2F%2Fgithub.com%2Forgs%2FLow-Price-Hosting%2Fpackages%2Fcontainer%2Fpackage%2Fcentos&search=Total%20downloads%3C%2Fspan%3E%5Cs%2A%3Ch3%20title%3D%22%28%5B0-9%2C%5D%2B%29%22%3E&replace=%241&label=GHCR%20downloads&color=0969da&style=flat-square)](https://github.com/orgs/Low-Price-Hosting/packages/container/package/centos) |
| [Alpine](https://github.com/Low-Price-Hosting/Alpine) | `ghcr.io/low-price-hosting/alpine` | [软件包](https://github.com/orgs/Low-Price-Hosting/packages/container/package/alpine) | [![alpine GHCR 下载次数](https://img.shields.io/badge/dynamic/regex?url=https%3A%2F%2Fgithub.com%2Forgs%2FLow-Price-Hosting%2Fpackages%2Fcontainer%2Fpackage%2Falpine&search=Total%20downloads%3C%2Fspan%3E%5Cs%2A%3Ch3%20title%3D%22%28%5B0-9%2C%5D%2B%29%22%3E&replace=%241&label=GHCR%20downloads&color=0969da&style=flat-square)](https://github.com/orgs/Low-Price-Hosting/packages/container/package/alpine) |
| [Fedora](https://github.com/Low-Price-Hosting/Fedora) | `ghcr.io/low-price-hosting/fedora` | [软件包](https://github.com/orgs/Low-Price-Hosting/packages/container/package/fedora) | [![fedora GHCR 下载次数](https://img.shields.io/badge/dynamic/regex?url=https%3A%2F%2Fgithub.com%2Forgs%2FLow-Price-Hosting%2Fpackages%2Fcontainer%2Fpackage%2Ffedora&search=Total%20downloads%3C%2Fspan%3E%5Cs%2A%3Ch3%20title%3D%22%28%5B0-9%2C%5D%2B%29%22%3E&replace=%241&label=GHCR%20downloads&color=0969da&style=flat-square)](https://github.com/orgs/Low-Price-Hosting/packages/container/package/fedora) |
| [AlmaLinux](https://github.com/Low-Price-Hosting/AlmaLinux) | `ghcr.io/low-price-hosting/almalinux` | [软件包](https://github.com/orgs/Low-Price-Hosting/packages/container/package/almalinux) | [![almalinux GHCR 下载次数](https://img.shields.io/badge/dynamic/regex?url=https%3A%2F%2Fgithub.com%2Forgs%2FLow-Price-Hosting%2Fpackages%2Fcontainer%2Fpackage%2Falmalinux&search=Total%20downloads%3C%2Fspan%3E%5Cs%2A%3Ch3%20title%3D%22%28%5B0-9%2C%5D%2B%29%22%3E&replace=%241&label=GHCR%20downloads&color=0969da&style=flat-square)](https://github.com/orgs/Low-Price-Hosting/packages/container/package/almalinux) |
| [Arch Linux](https://github.com/Low-Price-Hosting/ArchLinux) | `ghcr.io/low-price-hosting/archlinux` | [软件包](https://github.com/orgs/Low-Price-Hosting/packages/container/package/archlinux) | [![archlinux GHCR 下载次数](https://img.shields.io/badge/dynamic/regex?url=https%3A%2F%2Fgithub.com%2Forgs%2FLow-Price-Hosting%2Fpackages%2Fcontainer%2Fpackage%2Farchlinux&search=Total%20downloads%3C%2Fspan%3E%5Cs%2A%3Ch3%20title%3D%22%28%5B0-9%2C%5D%2B%29%22%3E&replace=%241&label=GHCR%20downloads&color=0969da&style=flat-square)](https://github.com/orgs/Low-Price-Hosting/packages/container/package/archlinux) |
| [Rocky Linux](https://github.com/Low-Price-Hosting/RockyLinux) | `ghcr.io/low-price-hosting/rockylinux` | [软件包](https://github.com/orgs/Low-Price-Hosting/packages/container/package/rockylinux) | [![rockylinux GHCR 下载次数](https://img.shields.io/badge/dynamic/regex?url=https%3A%2F%2Fgithub.com%2Forgs%2FLow-Price-Hosting%2Fpackages%2Fcontainer%2Fpackage%2Frockylinux&search=Total%20downloads%3C%2Fspan%3E%5Cs%2A%3Ch3%20title%3D%22%28%5B0-9%2C%5D%2B%29%22%3E&replace=%241&label=GHCR%20downloads&color=0969da&style=flat-square)](https://github.com/orgs/Low-Price-Hosting/packages/container/package/rockylinux) |

下载徽章显示 GitHub Packages 中的 **Total downloads（总下载量）**。各版本的下载量和已发布的架构列在对应的软件包页面上。缓存可能导致计数延迟；无法读取计数**不代表 0**。

<a id="versions-and-architectures"></a>

## 版本和架构参考

以下版本和架构参考来自 [2026 年 10 月 8 日的发现计划](https://github.com/Low-Price-Hosting/Container/actions/runs/37741062225)。这些是已发现的目标；请在所选标签的 **OS/Arch** 字段或 OCI 索引中确认已发布的架构。

| 发行版 | 版本 | 平台 — 带 `linux/` 前缀 |
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

\* 本计划未将 Rocky Linux 10 的 `riscv64` 目标纳入构建。架构集合可能因版本而异。

查看某个标签实际包含的架构：

```bash
docker buildx imagetools inspect ghcr.io/low-price-hosting/ubuntu:24.04
docker buildx imagetools inspect --raw ghcr.io/low-price-hosting/ubuntu:24.04
```

<a id="quick-start"></a>

## 快速使用

将示例中的 `24.04` 替换为您要使用的**已发布标签**。下载公开镜像无需登录 GHCR。

### 下载并运行

```bash
docker pull ghcr.io/low-price-hosting/ubuntu:24.04
docker run --rm -it ghcr.io/low-price-hosting/ubuntu:24.04 /bin/sh
```

Docker 会从多架构标签中选择与您的计算机架构匹配的镜像。

### 选择架构

```bash
docker pull --platform linux/arm64 ghcr.io/low-price-hosting/ubuntu:24.04

docker run --rm --platform linux/arm64 \
  ghcr.io/low-price-hosting/ubuntu:24.04 \
  /bin/sh -c 'cat /etc/os-release'
```

运行面向其他处理器系列的镜像需要相应的模拟支持。

### 使用摘要固定镜像

```bash
docker image inspect --format '{{json .RepoDigests}}' \
  ghcr.io/low-price-hosting/ubuntu:24.04

# 将 <digest> 替换为镜像的 SHA256 值。
docker pull ghcr.io/low-price-hosting/ubuntu@sha256:<digest>
```

版本标签可能更新；摘要可确保再次使用同一个镜像。

### 用于您自己的镜像

```dockerfile
FROM ghcr.io/low-price-hosting/ubuntu:24.04

COPY app/ /opt/app/
WORKDIR /opt/app
CMD ["/bin/sh"]
```

<a id="run-builds"></a>

## 启动构建

[操作 → 构建基础镜像 → 运行工作流](https://github.com/Low-Price-Hosting/Container/actions/workflows/build-base-images.yml)：

| 字段 | 用法 |
|---|---|
| `distribution` | `all` 或某个发行版名称。 |
| `version` | `all` 或确切版本，例如 `24.04`、`trixie`、`stream10` 或 `rolling`。 |
| `verify_only` | `true`：重新构建并测试，不发布。`false`：构建、测试并发布有变化或缺失的镜像。 |

将处理所选版本的所有已发现架构。使用 GitHub CLI：

```bash
# 为所有发行版构建并发布有变化或缺失的镜像。
gh workflow run build-base-images.yml \
  --repo Low-Price-Hosting/Container --ref main \
  -f distribution=all -f version=all -f verify_only=false

# 仅构建并测试 Fedora 镜像。
gh workflow run build-base-images.yml \
  --repo Low-Price-Hosting/Container --ref main \
  -f distribution=Fedora -f version=all -f verify_only=true
```

上方的构建徽章显示最近一次工作流的结果；仅验证的运行不会发布镜像。

<a id="pipeline"></a>

## 构建流程

```mermaid
flowchart LR
    D["版本和架构发现"] --> B["构建"]
    B --> T["测试"]
    T --> P["发布"]
    P --> G["GHCR 多架构镜像"]
```

| 阶段 | 对镜像执行的操作 |
|---|---|
| **构建** | 使用发行版的容器生成配方创建 rootfs/镜像。 |
| **测试** | 在独立的运行器上运行镜像；检查发行版标识、软件包管理器、架构和源码标签。 |
| **发布** | 某个版本的所有预期架构通过测试后，发布该版本的多架构标签。 |

每个构建/测试目标使用独立的运行器。测试属于基本运行检查，并非全面的应用兼容性测试。

新版本和架构会从源码目录清单中自动发现。相关配方、源码分支、引导镜像清单和软件包仓库准备就绪后，目标才会加入构建计划。源码通过每小时运行的 Cron 流程更新；GitHub 的调度可能延迟。

<a id="oci-metadata"></a>

## 标签和镜像信息

| 引用 | 含义 |
|---|---|
| `ubuntu:24.04`, `debian:trixie`, `centos:stream10` | 包含对应版本已通过测试架构的多架构标签。 |
| `latest` 和其他别名 | 根据发行版的版本目录确定的标签。 |
| `<image>@sha256:<digest>` | 不可变的镜像内容引用。 |

镜像的源码、版本和生成信息可在 OCI 元数据中查看：

```bash
docker image inspect --format '{{json .Config.Labels}}' \
  ghcr.io/low-price-hosting/ubuntu:24.04
```

`org.opencontainers.image.source` 指向源码配方仓库，`org.opencontainers.image.version` 表示版本，`io.low-price-hosting.build.source` 指向生成代码。可通过 `docker buildx imagetools inspect --raw` 读取多架构索引和架构注解。
