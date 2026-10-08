<div align="center">

**🌐 言語**

[Türkçe](../../README.md) · [English](README.en.md) · [简体中文](README.zh-CN.md) · [繁體中文](README.zh-TW.md) · **日本語** · [한국어](README.ko.md)

[Deutsch](README.de.md) · [Français](README.fr.md) · [Español](README.es.md) · [Português (Brasil)](README.pt-BR.md) · [Italiano](README.it.md) · [Русский](README.ru.md)

[Українська](README.uk.md) · [العربية](README.ar.md) · [فارسی](README.fa.md) · [हिन्दी](README.hi.md) · [Bahasa Indonesia](README.id.md) · [Tiếng Việt](README.vi.md)

</div>

---

# Low-Price-Hosting · Container

**Linux のベースコンテナイメージ — ソースレシピからビルドし、アーキテクチャごとにテストして GHCR に公開します。**

[![ビルド状況](https://github.com/Low-Price-Hosting/Container/actions/workflows/build-base-images.yml/badge.svg?branch=main)](https://github.com/Low-Price-Hosting/Container/actions/workflows/build-base-images.yml)
[![ソースの更新](https://github.com/Low-Price-Hosting/Cron/actions/workflows/mirror-container-sources.yml/badge.svg?branch=main)](https://github.com/Low-Price-Hosting/Cron/actions/workflows/mirror-container-sources.yml)
[![レジストリ：GHCR](https://img.shields.io/badge/registry-GHCR-0969da?style=flat-square)](https://github.com/orgs/Low-Price-Hosting/packages?ecosystem=container)

**8 ディストリビューション** · **動的なバージョンとアーキテクチャ** · **ビルド → テスト → 公開**

[イメージ](#images-and-downloads) · [アーキテクチャ](#versions-and-architectures) · [使い方](#quick-start) · [ビルドの開始](#run-builds) · [ビルドの流れ](#pipeline) · [イメージ情報](#oci-metadata)

---

<a id="images-and-downloads"></a>

## イメージとダウンロード数

| ディストリビューション | イメージ参照 | タグと OS/Arch | 総ダウンロード数 |
|---|---|---|---|
| [Ubuntu](https://github.com/Low-Price-Hosting/Ubuntu) | `ghcr.io/low-price-hosting/ubuntu` | [パッケージ](https://github.com/orgs/Low-Price-Hosting/packages/container/package/ubuntu) | [![ubuntu の GHCR ダウンロード数](https://img.shields.io/badge/dynamic/regex?url=https%3A%2F%2Fgithub.com%2Forgs%2FLow-Price-Hosting%2Fpackages%2Fcontainer%2Fpackage%2Fubuntu&search=Total%20downloads%3C%2Fspan%3E%5Cs%2A%3Ch3%20title%3D%22%28%5B0-9%2C%5D%2B%29%22%3E&replace=%241&label=GHCR%20downloads&color=0969da&style=flat-square)](https://github.com/orgs/Low-Price-Hosting/packages/container/package/ubuntu) |
| [Debian](https://github.com/Low-Price-Hosting/Debian) | `ghcr.io/low-price-hosting/debian` | [パッケージ](https://github.com/orgs/Low-Price-Hosting/packages/container/package/debian) | [![debian の GHCR ダウンロード数](https://img.shields.io/badge/dynamic/regex?url=https%3A%2F%2Fgithub.com%2Forgs%2FLow-Price-Hosting%2Fpackages%2Fcontainer%2Fpackage%2Fdebian&search=Total%20downloads%3C%2Fspan%3E%5Cs%2A%3Ch3%20title%3D%22%28%5B0-9%2C%5D%2B%29%22%3E&replace=%241&label=GHCR%20downloads&color=0969da&style=flat-square)](https://github.com/orgs/Low-Price-Hosting/packages/container/package/debian) |
| [CentOS Stream](https://github.com/Low-Price-Hosting/Centos) | `ghcr.io/low-price-hosting/centos` | [パッケージ](https://github.com/orgs/Low-Price-Hosting/packages/container/package/centos) | [![centos の GHCR ダウンロード数](https://img.shields.io/badge/dynamic/regex?url=https%3A%2F%2Fgithub.com%2Forgs%2FLow-Price-Hosting%2Fpackages%2Fcontainer%2Fpackage%2Fcentos&search=Total%20downloads%3C%2Fspan%3E%5Cs%2A%3Ch3%20title%3D%22%28%5B0-9%2C%5D%2B%29%22%3E&replace=%241&label=GHCR%20downloads&color=0969da&style=flat-square)](https://github.com/orgs/Low-Price-Hosting/packages/container/package/centos) |
| [Alpine](https://github.com/Low-Price-Hosting/Alpine) | `ghcr.io/low-price-hosting/alpine` | [パッケージ](https://github.com/orgs/Low-Price-Hosting/packages/container/package/alpine) | [![alpine の GHCR ダウンロード数](https://img.shields.io/badge/dynamic/regex?url=https%3A%2F%2Fgithub.com%2Forgs%2FLow-Price-Hosting%2Fpackages%2Fcontainer%2Fpackage%2Falpine&search=Total%20downloads%3C%2Fspan%3E%5Cs%2A%3Ch3%20title%3D%22%28%5B0-9%2C%5D%2B%29%22%3E&replace=%241&label=GHCR%20downloads&color=0969da&style=flat-square)](https://github.com/orgs/Low-Price-Hosting/packages/container/package/alpine) |
| [Fedora](https://github.com/Low-Price-Hosting/Fedora) | `ghcr.io/low-price-hosting/fedora` | [パッケージ](https://github.com/orgs/Low-Price-Hosting/packages/container/package/fedora) | [![fedora の GHCR ダウンロード数](https://img.shields.io/badge/dynamic/regex?url=https%3A%2F%2Fgithub.com%2Forgs%2FLow-Price-Hosting%2Fpackages%2Fcontainer%2Fpackage%2Ffedora&search=Total%20downloads%3C%2Fspan%3E%5Cs%2A%3Ch3%20title%3D%22%28%5B0-9%2C%5D%2B%29%22%3E&replace=%241&label=GHCR%20downloads&color=0969da&style=flat-square)](https://github.com/orgs/Low-Price-Hosting/packages/container/package/fedora) |
| [AlmaLinux](https://github.com/Low-Price-Hosting/AlmaLinux) | `ghcr.io/low-price-hosting/almalinux` | [パッケージ](https://github.com/orgs/Low-Price-Hosting/packages/container/package/almalinux) | [![almalinux の GHCR ダウンロード数](https://img.shields.io/badge/dynamic/regex?url=https%3A%2F%2Fgithub.com%2Forgs%2FLow-Price-Hosting%2Fpackages%2Fcontainer%2Fpackage%2Falmalinux&search=Total%20downloads%3C%2Fspan%3E%5Cs%2A%3Ch3%20title%3D%22%28%5B0-9%2C%5D%2B%29%22%3E&replace=%241&label=GHCR%20downloads&color=0969da&style=flat-square)](https://github.com/orgs/Low-Price-Hosting/packages/container/package/almalinux) |
| [Arch Linux](https://github.com/Low-Price-Hosting/ArchLinux) | `ghcr.io/low-price-hosting/archlinux` | [パッケージ](https://github.com/orgs/Low-Price-Hosting/packages/container/package/archlinux) | [![archlinux の GHCR ダウンロード数](https://img.shields.io/badge/dynamic/regex?url=https%3A%2F%2Fgithub.com%2Forgs%2FLow-Price-Hosting%2Fpackages%2Fcontainer%2Fpackage%2Farchlinux&search=Total%20downloads%3C%2Fspan%3E%5Cs%2A%3Ch3%20title%3D%22%28%5B0-9%2C%5D%2B%29%22%3E&replace=%241&label=GHCR%20downloads&color=0969da&style=flat-square)](https://github.com/orgs/Low-Price-Hosting/packages/container/package/archlinux) |
| [Rocky Linux](https://github.com/Low-Price-Hosting/RockyLinux) | `ghcr.io/low-price-hosting/rockylinux` | [パッケージ](https://github.com/orgs/Low-Price-Hosting/packages/container/package/rockylinux) | [![rockylinux の GHCR ダウンロード数](https://img.shields.io/badge/dynamic/regex?url=https%3A%2F%2Fgithub.com%2Forgs%2FLow-Price-Hosting%2Fpackages%2Fcontainer%2Fpackage%2Frockylinux&search=Total%20downloads%3C%2Fspan%3E%5Cs%2A%3Ch3%20title%3D%22%28%5B0-9%2C%5D%2B%29%22%3E&replace=%241&label=GHCR%20downloads&color=0969da&style=flat-square)](https://github.com/orgs/Low-Price-Hosting/packages/container/package/rockylinux) |

ダウンロードバッジは GitHub Packages の **Total downloads（総ダウンロード数）** を表示します。バージョンごとのダウンロード数と公開済みのアーキテクチャは、各パッケージページで確認できます。キャッシュによりカウンターの更新が遅れる場合があります。読み取れないカウンターは **0 を意味しません**。

<a id="versions-and-architectures"></a>

## バージョンとアーキテクチャの参考情報

[2026 年 10 月 8 日の検出計画](https://github.com/Low-Price-Hosting/Container/actions/runs/37741062225)に基づくバージョンとアーキテクチャの参考情報です。これらは検出されたターゲットです。公開済みのアーキテクチャは、選択したタグの **OS/Arch** 欄または OCI インデックスで確認してください。

| ディストリビューション | バージョン | プラットフォーム — `linux/` プレフィックス付き |
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

\* この計画では Rocky Linux 10 の `riscv64` ターゲットはビルド対象から除外されました。アーキテクチャの構成はバージョンによって異なる場合があります。

タグに実際に含まれるアーキテクチャを確認します：

```bash
docker buildx imagetools inspect ghcr.io/low-price-hosting/ubuntu:24.04
docker buildx imagetools inspect --raw ghcr.io/low-price-hosting/ubuntu:24.04
```

<a id="quick-start"></a>

## クイックスタート

例の `24.04` を、使用したい**公開済みのタグ**に置き換えてください。公開イメージのダウンロードに GHCR へのログインは必要ありません。

### ダウンロードして実行する

```bash
docker pull ghcr.io/low-price-hosting/ubuntu:24.04
docker run --rm -it ghcr.io/low-price-hosting/ubuntu:24.04 /bin/sh
```

Docker はマルチアーキテクチャタグから、お使いのコンピューターのアーキテクチャに合うイメージを選択します。

### アーキテクチャを選択する

```bash
docker pull --platform linux/arm64 ghcr.io/low-price-hosting/ubuntu:24.04

docker run --rm --platform linux/arm64 \
  ghcr.io/low-price-hosting/ubuntu:24.04 \
  /bin/sh -c 'cat /etc/os-release'
```

異なるプロセッサーファミリー向けのイメージを実行するには、適切なエミュレーションが必要です。

### ダイジェストで固定する

```bash
docker image inspect --format '{{json .RepoDigests}}' \
  ghcr.io/low-price-hosting/ubuntu:24.04

# <digest> をイメージの SHA256 値に置き換えてください。
docker pull ghcr.io/low-price-hosting/ubuntu@sha256:<digest>
```

バージョンタグは更新される場合があります。ダイジェストを使うと同じイメージを再利用できます。

### 自分のイメージで使う

```dockerfile
FROM ghcr.io/low-price-hosting/ubuntu:24.04

COPY app/ /opt/app/
WORKDIR /opt/app
CMD ["/bin/sh"]
```

<a id="run-builds"></a>

## ビルドの開始

[アクション → ベースイメージをビルド → ワークフローを実行](https://github.com/Low-Price-Hosting/Container/actions/workflows/build-base-images.yml)：

| 項目 | 使い方 |
|---|---|
| `distribution` | `all` またはディストリビューション名。 |
| `version` | `all` または `24.04`、`trixie`、`stream10`、`rolling` などの正確なバージョン。 |
| `verify_only` | `true`：再ビルドしてテストします。公開はしません。`false`：変更されたイメージや不足しているイメージをビルドし、テストして公開します。 |

選択したバージョンで検出されたすべてのアーキテクチャを処理します。GitHub CLI を使う場合：

```bash
# 全ディストリビューションで、変更されたイメージや不足しているイメージをビルドして公開します。
gh workflow run build-base-images.yml \
  --repo Low-Price-Hosting/Container --ref main \
  -f distribution=all -f version=all -f verify_only=false

# Fedora イメージのビルドとテストのみを行います。
gh workflow run build-base-images.yml \
  --repo Low-Price-Hosting/Container --ref main \
  -f distribution=Fedora -f version=all -f verify_only=true
```

上部のビルドバッジは最新のワークフロー結果を表示します。検証のみの実行ではイメージは公開されません。

<a id="pipeline"></a>

## ビルドの流れ

```mermaid
flowchart LR
    D["バージョンとアーキテクチャの検出"] --> B["ビルド"]
    B --> T["テスト"]
    T --> P["公開"]
    P --> G["GHCR マルチアーキテクチャイメージ"]
```

| 段階 | イメージに対する処理 |
|---|---|
| **ビルド** | ディストリビューションのコンテナ生成レシピを使って rootfs/イメージを作成します。 |
| **テスト** | 別のランナーでイメージを実行し、ディストリビューション ID、パッケージマネージャー、アーキテクチャ、ソースラベルを確認します。 |
| **公開** | バージョンごとに、想定されるすべてのアーキテクチャがテストに合格した時点でマルチアーキテクチャのバージョンタグを公開します。 |

各ビルド/テストターゲットは個別のランナーを使用します。テストは基本的な動作確認であり、アプリケーションの互換性を包括的に検証するものではありません。

新しいバージョンとアーキテクチャはソースカタログから自動的に検出されます。関連するレシピ、ソースブランチ、ブートストラップマニフェスト、パッケージリポジトリが準備できた時点でビルド計画に追加されます。ソースは毎時実行される Cron の処理で更新されます。GitHub のスケジュール実行には遅延が生じる場合があります。

<a id="oci-metadata"></a>

## タグとイメージ情報

| 参照 | 意味 |
|---|---|
| `ubuntu:24.04`, `debian:trixie`, `centos:stream10` | 該当バージョンのテスト済みアーキテクチャを含むマルチアーキテクチャタグ。 |
| `latest` とその他のエイリアス | ディストリビューションのバージョンカタログに基づいて決まるタグ。 |
| `<image>@sha256:<digest>` | イメージ内容への不変の参照。 |

イメージのソース、バージョン、生成情報は OCI メタデータに含まれます：

```bash
docker image inspect --format '{{json .Config.Labels}}' \
  ghcr.io/low-price-hosting/ubuntu:24.04
```

`org.opencontainers.image.source` はソースレシピのリポジトリ、`org.opencontainers.image.version` はバージョン、`io.low-price-hosting.build.source` は生成コードを示します。マルチアーキテクチャのインデックスとアーキテクチャのアノテーションは `docker buildx imagetools inspect --raw` で読み取れます。
