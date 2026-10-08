<div align="center">

**🌐 Idiomas**

[Türkçe](../../README.md) · [English](README.en.md) · [简体中文](README.zh-CN.md) · [繁體中文](README.zh-TW.md) · [日本語](README.ja.md) · [한국어](README.ko.md)

[Deutsch](README.de.md) · [Français](README.fr.md) · [Español](README.es.md) · **Português (Brasil)** · [Italiano](README.it.md) · [Русский](README.ru.md)

[Українська](README.uk.md) · [العربية](README.ar.md) · [فارسی](README.fa.md) · [हिन्दी](README.hi.md) · [Bahasa Indonesia](README.id.md) · [Tiếng Việt](README.vi.md)

</div>

---

# Low-Price-Hosting · Container

**Imagens base de Linux para contêineres — construção a partir das receitas de origem, testes por arquitetura e publicação no GHCR.**

[![Status da construção](https://github.com/Low-Price-Hosting/Container/actions/workflows/build-base-images.yml/badge.svg?branch=main)](https://github.com/Low-Price-Hosting/Container/actions/workflows/build-base-images.yml)
[![Atualizações das fontes](https://github.com/Low-Price-Hosting/Cron/actions/workflows/mirror-container-sources.yml/badge.svg?branch=main)](https://github.com/Low-Price-Hosting/Cron/actions/workflows/mirror-container-sources.yml)
[![Registro: GHCR](https://img.shields.io/badge/registry-GHCR-0969da?style=flat-square)](https://github.com/orgs/Low-Price-Hosting/packages?ecosystem=container)

**8 distribuições** · **Versões e arquiteturas dinâmicas** · **Construir → Testar → Publicar**

[Imagens](#images-and-downloads) · [Arquiteturas](#versions-and-architectures) · [Uso](#quick-start) · [Iniciar construções](#run-builds) · [Fluxo de construção](#pipeline) · [Informações das imagens](#oci-metadata)

---

<a id="images-and-downloads"></a>

## Imagens e downloads

| Distribuição | Referência da imagem | Tags e OS/Arch | Total de downloads |
|---|---|---|---|
| [Ubuntu](https://github.com/Low-Price-Hosting/Ubuntu) | `ghcr.io/low-price-hosting/ubuntu` | [Pacotes](https://github.com/orgs/Low-Price-Hosting/packages/container/package/ubuntu) | [![ubuntu número de downloads do GHCR](https://img.shields.io/badge/dynamic/regex?url=https%3A%2F%2Fgithub.com%2Forgs%2FLow-Price-Hosting%2Fpackages%2Fcontainer%2Fpackage%2Fubuntu&search=Total%20downloads%3C%2Fspan%3E%5Cs%2A%3Ch3%20title%3D%22%28%5B0-9%2C%5D%2B%29%22%3E&replace=%241&label=GHCR%20downloads&color=0969da&style=flat-square)](https://github.com/orgs/Low-Price-Hosting/packages/container/package/ubuntu) |
| [Debian](https://github.com/Low-Price-Hosting/Debian) | `ghcr.io/low-price-hosting/debian` | [Pacotes](https://github.com/orgs/Low-Price-Hosting/packages/container/package/debian) | [![debian número de downloads do GHCR](https://img.shields.io/badge/dynamic/regex?url=https%3A%2F%2Fgithub.com%2Forgs%2FLow-Price-Hosting%2Fpackages%2Fcontainer%2Fpackage%2Fdebian&search=Total%20downloads%3C%2Fspan%3E%5Cs%2A%3Ch3%20title%3D%22%28%5B0-9%2C%5D%2B%29%22%3E&replace=%241&label=GHCR%20downloads&color=0969da&style=flat-square)](https://github.com/orgs/Low-Price-Hosting/packages/container/package/debian) |
| [CentOS Stream](https://github.com/Low-Price-Hosting/Centos) | `ghcr.io/low-price-hosting/centos` | [Pacotes](https://github.com/orgs/Low-Price-Hosting/packages/container/package/centos) | [![centos número de downloads do GHCR](https://img.shields.io/badge/dynamic/regex?url=https%3A%2F%2Fgithub.com%2Forgs%2FLow-Price-Hosting%2Fpackages%2Fcontainer%2Fpackage%2Fcentos&search=Total%20downloads%3C%2Fspan%3E%5Cs%2A%3Ch3%20title%3D%22%28%5B0-9%2C%5D%2B%29%22%3E&replace=%241&label=GHCR%20downloads&color=0969da&style=flat-square)](https://github.com/orgs/Low-Price-Hosting/packages/container/package/centos) |
| [Alpine](https://github.com/Low-Price-Hosting/Alpine) | `ghcr.io/low-price-hosting/alpine` | [Pacotes](https://github.com/orgs/Low-Price-Hosting/packages/container/package/alpine) | [![alpine número de downloads do GHCR](https://img.shields.io/badge/dynamic/regex?url=https%3A%2F%2Fgithub.com%2Forgs%2FLow-Price-Hosting%2Fpackages%2Fcontainer%2Fpackage%2Falpine&search=Total%20downloads%3C%2Fspan%3E%5Cs%2A%3Ch3%20title%3D%22%28%5B0-9%2C%5D%2B%29%22%3E&replace=%241&label=GHCR%20downloads&color=0969da&style=flat-square)](https://github.com/orgs/Low-Price-Hosting/packages/container/package/alpine) |
| [Fedora](https://github.com/Low-Price-Hosting/Fedora) | `ghcr.io/low-price-hosting/fedora` | [Pacotes](https://github.com/orgs/Low-Price-Hosting/packages/container/package/fedora) | [![fedora número de downloads do GHCR](https://img.shields.io/badge/dynamic/regex?url=https%3A%2F%2Fgithub.com%2Forgs%2FLow-Price-Hosting%2Fpackages%2Fcontainer%2Fpackage%2Ffedora&search=Total%20downloads%3C%2Fspan%3E%5Cs%2A%3Ch3%20title%3D%22%28%5B0-9%2C%5D%2B%29%22%3E&replace=%241&label=GHCR%20downloads&color=0969da&style=flat-square)](https://github.com/orgs/Low-Price-Hosting/packages/container/package/fedora) |
| [AlmaLinux](https://github.com/Low-Price-Hosting/AlmaLinux) | `ghcr.io/low-price-hosting/almalinux` | [Pacotes](https://github.com/orgs/Low-Price-Hosting/packages/container/package/almalinux) | [![almalinux número de downloads do GHCR](https://img.shields.io/badge/dynamic/regex?url=https%3A%2F%2Fgithub.com%2Forgs%2FLow-Price-Hosting%2Fpackages%2Fcontainer%2Fpackage%2Falmalinux&search=Total%20downloads%3C%2Fspan%3E%5Cs%2A%3Ch3%20title%3D%22%28%5B0-9%2C%5D%2B%29%22%3E&replace=%241&label=GHCR%20downloads&color=0969da&style=flat-square)](https://github.com/orgs/Low-Price-Hosting/packages/container/package/almalinux) |
| [Arch Linux](https://github.com/Low-Price-Hosting/ArchLinux) | `ghcr.io/low-price-hosting/archlinux` | [Pacotes](https://github.com/orgs/Low-Price-Hosting/packages/container/package/archlinux) | [![archlinux número de downloads do GHCR](https://img.shields.io/badge/dynamic/regex?url=https%3A%2F%2Fgithub.com%2Forgs%2FLow-Price-Hosting%2Fpackages%2Fcontainer%2Fpackage%2Farchlinux&search=Total%20downloads%3C%2Fspan%3E%5Cs%2A%3Ch3%20title%3D%22%28%5B0-9%2C%5D%2B%29%22%3E&replace=%241&label=GHCR%20downloads&color=0969da&style=flat-square)](https://github.com/orgs/Low-Price-Hosting/packages/container/package/archlinux) |
| [Rocky Linux](https://github.com/Low-Price-Hosting/RockyLinux) | `ghcr.io/low-price-hosting/rockylinux` | [Pacotes](https://github.com/orgs/Low-Price-Hosting/packages/container/package/rockylinux) | [![rockylinux número de downloads do GHCR](https://img.shields.io/badge/dynamic/regex?url=https%3A%2F%2Fgithub.com%2Forgs%2FLow-Price-Hosting%2Fpackages%2Fcontainer%2Fpackage%2Frockylinux&search=Total%20downloads%3C%2Fspan%3E%5Cs%2A%3Ch3%20title%3D%22%28%5B0-9%2C%5D%2B%29%22%3E&replace=%241&label=GHCR%20downloads&color=0969da&style=flat-square)](https://github.com/orgs/Low-Price-Hosting/packages/container/package/rockylinux) |

Os indicadores de download mostram o valor **Total de downloads** do GitHub Packages. Os downloads por versão e as arquiteturas publicadas estão na página do pacote correspondente. O cache pode atrasar os contadores; um contador ilegível não significa **0**.

<a id="versions-and-architectures"></a>

## Referências de versões e arquiteturas

Referências de versões e arquiteturas do [plano de descoberta de 8 de outubro de 2026](https://github.com/Low-Price-Hosting/Container/actions/runs/37741062225). Estes são os alvos descobertos; confira as arquiteturas publicadas no campo **OS/Arch** da tag escolhida ou no índice OCI.

| Distribuição | Versões | Plataformas — com o prefixo `linux/` |
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

\* O alvo `riscv64` do Rocky Linux 10 ficou fora da construção neste plano. O conjunto de arquiteturas pode variar conforme a versão.

Inspecione as arquiteturas reais de uma tag:

```bash
docker buildx imagetools inspect ghcr.io/low-price-hosting/ubuntu:24.04
docker buildx imagetools inspect --raw ghcr.io/low-price-hosting/ubuntu:24.04
```

<a id="quick-start"></a>

## Uso rápido

Substitua `24.04` nos exemplos pela **tag publicada** que deseja usar. Não é necessário fazer login no GHCR para baixar imagens públicas.

### Baixar e executar

```bash
docker pull ghcr.io/low-price-hosting/ubuntu:24.04
docker run --rm -it ghcr.io/low-price-hosting/ubuntu:24.04 /bin/sh
```

O Docker seleciona na tag multiarquitetura a imagem adequada à arquitetura do seu computador.

### Escolher uma arquitetura

```bash
docker pull --platform linux/arm64 ghcr.io/low-price-hosting/ubuntu:24.04

docker run --rm --platform linux/arm64 \
  ghcr.io/low-price-hosting/ubuntu:24.04 \
  /bin/sh -c 'cat /etc/os-release'
```

Para executar uma imagem de outra família de processadores, é necessária uma emulação adequada.

### Fixar pelo digest

```bash
docker image inspect --format '{{json .RepoDigests}}' \
  ghcr.io/low-price-hosting/ubuntu:24.04

# Substitua <digest> pelo valor SHA256 da imagem.
docker pull ghcr.io/low-price-hosting/ubuntu@sha256:<digest>
```

As tags de versão podem ser atualizadas; o digest permite reutilizar a mesma imagem.

### Usar na sua própria imagem

```dockerfile
FROM ghcr.io/low-price-hosting/ubuntu:24.04

COPY app/ /opt/app/
WORKDIR /opt/app
CMD ["/bin/sh"]
```

<a id="run-builds"></a>

## Iniciar construções

[Actions → Construir imagens base → Executar fluxo de trabalho](https://github.com/Low-Price-Hosting/Container/actions/workflows/build-base-images.yml):

| Campo | Uso |
|---|---|
| `distribution` | `all` ou o nome de uma distribuição. |
| `version` | `all` ou uma versão exata, como `24.04`, `trixie`, `stream10` ou `rolling`. |
| `verify_only` | `true`: reconstruir/testar sem publicar. `false`: construir/testar e publicar as imagens alteradas ou ausentes. |

Todas as arquiteturas descobertas da versão selecionada são processadas. Com a CLI do GitHub:

```bash
# Construir e publicar as imagens alteradas ou ausentes de todas as distribuições.
gh workflow run build-base-images.yml \
  --repo Low-Price-Hosting/Container --ref main \
  -f distribution=all -f version=all -f verify_only=false

# Apenas construir e testar as imagens do Fedora.
gh workflow run build-base-images.yml \
  --repo Low-Price-Hosting/Container --ref main \
  -f distribution=Fedora -f version=all -f verify_only=true
```

O indicador de construção acima mostra o resultado do último fluxo de trabalho; uma execução apenas de verificação não publica imagens.

<a id="pipeline"></a>

## Fluxo de construção

```mermaid
flowchart LR
    D["Descoberta de versões e arquiteturas"] --> B["Construir"]
    B --> T["Testar"]
    T --> P["Publicar"]
    P --> G["Imagem multiarquitetura no GHCR"]
```

| Etapa | Operação realizada na imagem |
|---|---|
| **Construir** | O rootfs/a imagem é criado com a receita de construção de contêineres da distribuição. |
| **Testar** | A imagem é executada em um runner separado; são verificados a identidade da distribuição, o gerenciador de pacotes, a arquitetura e o rótulo de origem. |
| **Publicar** | A tag de versão multiarquitetura é publicada quando todas as arquiteturas esperadas da versão passam nos testes. |

Cada alvo de construção/teste usa um runner separado. Os testes verificam o funcionamento básico; não são testes abrangentes de compatibilidade de aplicações.

Novas versões e arquiteturas são descobertas automaticamente nos catálogos de origem. Elas entram no plano de construção quando a receita correspondente, a branch de origem, o manifesto de inicialização e os repositórios de pacotes estão prontos. As fontes são atualizadas pelo fluxo Cron a cada hora; o agendamento do GitHub pode sofrer atrasos.

<a id="oci-metadata"></a>

## Tags e informações das imagens

| Referência | Significado |
|---|---|
| `ubuntu:24.04`, `debian:trixie`, `centos:stream10` | Tag multiarquitetura com as arquiteturas testadas da versão correspondente. |
| `latest` e outros aliases | Tags definidas conforme o catálogo de versões da distribuição. |
| `<image>@sha256:<digest>` | Referência imutável ao conteúdo da imagem. |

As informações de origem, versão e construção da imagem estão nos metadados OCI:

```bash
docker image inspect --format '{{json .Config.Labels}}' \
  ghcr.io/low-price-hosting/ubuntu:24.04
```

`org.opencontainers.image.source` indica o repositório da receita de origem, `org.opencontainers.image.version` a versão e `io.low-price-hosting.build.source` o código de construção. O índice multiarquitetura e as anotações de arquitetura podem ser consultados com `docker buildx imagetools inspect --raw`.
