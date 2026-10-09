<div align="center">

**🌐 भाषाएँ**

[Türkçe](../../README.md) · [English](README.en.md) · [简体中文](README.zh-CN.md) · [繁體中文](README.zh-TW.md) · [日本語](README.ja.md) · [한국어](README.ko.md)

[Deutsch](README.de.md) · [Français](README.fr.md) · [Español](README.es.md) · [Português (Brasil)](README.pt-BR.md) · [Italiano](README.it.md) · [Русский](README.ru.md)

[Українська](README.uk.md) · [العربية](README.ar.md) · [فارسی](README.fa.md) · **हिन्दी** · [Bahasa Indonesia](README.id.md) · [Tiếng Việt](README.vi.md)

</div>

---

# Low-Price-Hosting · Container

**Linux के बेस कंटेनर इमेज — स्रोत की बिल्ड रेसिपी से तैयार, हर आर्किटेक्चर पर परीक्षण किए गए और GHCR, Docker Hub और Quay पर प्रकाशित।**

[![बिल्ड की स्थिति](https://github.com/Low-Price-Hosting/Container/actions/workflows/build-base-images.yml/badge.svg?branch=main)](https://github.com/Low-Price-Hosting/Container/actions/workflows/build-base-images.yml)
[![स्रोत अपडेट](https://github.com/Low-Price-Hosting/Cron/actions/workflows/mirror-container-sources.yml/badge.svg?branch=main)](https://github.com/Low-Price-Hosting/Cron/actions/workflows/mirror-container-sources.yml)
[![रजिस्ट्री: GHCR](https://img.shields.io/badge/registry-GHCR-0969da?style=flat-square)](https://github.com/orgs/Low-Price-Hosting/packages?ecosystem=container)
[![रजिस्ट्री: Docker Hub](https://img.shields.io/badge/registry-Docker_Hub-2496ed?style=flat-square)](https://hub.docker.com/u/lphllc)
[![रजिस्ट्री: Quay](https://img.shields.io/badge/registry-Quay-ee0000?style=flat-square)](https://quay.io/organization/lowpricehosting)

**8 वितरण** · **गतिशील संस्करण और आर्किटेक्चर** · **बिल्ड → परीक्षण → प्रकाशन**

[इमेज](#images-and-downloads) · [आर्किटेक्चर](#versions-and-architectures) · [उपयोग](#quick-start) · [बिल्ड शुरू करना](#run-builds) · [इमेज की जानकारी](#oci-metadata)

---

<a id="images-and-downloads"></a>

## इमेज और डाउनलोड

| वितरण | GHCR | Docker Hub | Quay |
|---|---|---|---|
| [Ubuntu](https://github.com/Low-Price-Hosting/Ubuntu) | [![ubuntu के GHCR डाउनलोड की संख्या](https://img.shields.io/badge/dynamic/regex?url=https%3A%2F%2Fgithub.com%2Forgs%2FLow-Price-Hosting%2Fpackages%2Fcontainer%2Fpackage%2Fubuntu&search=Total%20downloads%3C%2Fspan%3E%5Cs%2A%3Ch3%20title%3D%22%28%5B0-9%2C%5D%2B%29%22%3E&replace=%241&label=GHCR%20downloads&color=0969da&style=flat-square&cacheSeconds=300)](https://github.com/orgs/Low-Price-Hosting/packages/container/package/ubuntu) | [![ubuntu Docker Hub pulls](https://img.shields.io/docker/pulls/lphllc/ubuntu?label=Docker%20pulls&style=flat-square)](https://hub.docker.com/r/lphllc/ubuntu) | [![ubuntu Quay architectures](https://img.shields.io/badge/dynamic/json?url=https%3A%2F%2Fquay.io%2Fapi%2Fv1%2Frepository%2Flowpricehosting%2Fubuntu%2Ftag%2F%3FspecificTag%3Dlatest%26onlyActiveTags%3Dtrue&query=%24.tags%5B0%5D.child_manifest_count&label=Quay%20architectures&color=ee0000&style=flat-square&cacheSeconds=300)](https://quay.io/repository/lowpricehosting/ubuntu?tab=tags) |
| [Debian](https://github.com/Low-Price-Hosting/Debian) | [![debian के GHCR डाउनलोड की संख्या](https://img.shields.io/badge/dynamic/regex?url=https%3A%2F%2Fgithub.com%2Forgs%2FLow-Price-Hosting%2Fpackages%2Fcontainer%2Fpackage%2Fdebian&search=Total%20downloads%3C%2Fspan%3E%5Cs%2A%3Ch3%20title%3D%22%28%5B0-9%2C%5D%2B%29%22%3E&replace=%241&label=GHCR%20downloads&color=0969da&style=flat-square&cacheSeconds=300)](https://github.com/orgs/Low-Price-Hosting/packages/container/package/debian) | [![debian Docker Hub pulls](https://img.shields.io/docker/pulls/lphllc/debian?label=Docker%20pulls&style=flat-square)](https://hub.docker.com/r/lphllc/debian) | [![debian Quay architectures](https://img.shields.io/badge/dynamic/json?url=https%3A%2F%2Fquay.io%2Fapi%2Fv1%2Frepository%2Flowpricehosting%2Fdebian%2Ftag%2F%3FspecificTag%3Dlatest%26onlyActiveTags%3Dtrue&query=%24.tags%5B0%5D.child_manifest_count&label=Quay%20architectures&color=ee0000&style=flat-square&cacheSeconds=300)](https://quay.io/repository/lowpricehosting/debian?tab=tags) |
| [CentOS Stream](https://github.com/Low-Price-Hosting/Centos) | [![centos के GHCR डाउनलोड की संख्या](https://img.shields.io/badge/dynamic/regex?url=https%3A%2F%2Fgithub.com%2Forgs%2FLow-Price-Hosting%2Fpackages%2Fcontainer%2Fpackage%2Fcentos&search=Total%20downloads%3C%2Fspan%3E%5Cs%2A%3Ch3%20title%3D%22%28%5B0-9%2C%5D%2B%29%22%3E&replace=%241&label=GHCR%20downloads&color=0969da&style=flat-square&cacheSeconds=300)](https://github.com/orgs/Low-Price-Hosting/packages/container/package/centos) | [![centos Docker Hub pulls](https://img.shields.io/docker/pulls/lphllc/centos?label=Docker%20pulls&style=flat-square)](https://hub.docker.com/r/lphllc/centos) | [![centos Quay architectures](https://img.shields.io/badge/dynamic/json?url=https%3A%2F%2Fquay.io%2Fapi%2Fv1%2Frepository%2Flowpricehosting%2Fcentos%2Ftag%2F%3FspecificTag%3Dlatest%26onlyActiveTags%3Dtrue&query=%24.tags%5B0%5D.child_manifest_count&label=Quay%20architectures&color=ee0000&style=flat-square&cacheSeconds=300)](https://quay.io/repository/lowpricehosting/centos?tab=tags) |
| [Alpine](https://github.com/Low-Price-Hosting/Alpine) | [![alpine के GHCR डाउनलोड की संख्या](https://img.shields.io/badge/dynamic/regex?url=https%3A%2F%2Fgithub.com%2Forgs%2FLow-Price-Hosting%2Fpackages%2Fcontainer%2Fpackage%2Falpine&search=Total%20downloads%3C%2Fspan%3E%5Cs%2A%3Ch3%20title%3D%22%28%5B0-9%2C%5D%2B%29%22%3E&replace=%241&label=GHCR%20downloads&color=0969da&style=flat-square&cacheSeconds=300)](https://github.com/orgs/Low-Price-Hosting/packages/container/package/alpine) | [![alpine Docker Hub pulls](https://img.shields.io/docker/pulls/lphllc/alpine?label=Docker%20pulls&style=flat-square)](https://hub.docker.com/r/lphllc/alpine) | [![alpine Quay architectures](https://img.shields.io/badge/dynamic/json?url=https%3A%2F%2Fquay.io%2Fapi%2Fv1%2Frepository%2Flowpricehosting%2Falpine%2Ftag%2F%3FspecificTag%3Dlatest%26onlyActiveTags%3Dtrue&query=%24.tags%5B0%5D.child_manifest_count&label=Quay%20architectures&color=ee0000&style=flat-square&cacheSeconds=300)](https://quay.io/repository/lowpricehosting/alpine?tab=tags) |
| [Fedora](https://github.com/Low-Price-Hosting/Fedora) | [![fedora के GHCR डाउनलोड की संख्या](https://img.shields.io/badge/dynamic/regex?url=https%3A%2F%2Fgithub.com%2Forgs%2FLow-Price-Hosting%2Fpackages%2Fcontainer%2Fpackage%2Ffedora&search=Total%20downloads%3C%2Fspan%3E%5Cs%2A%3Ch3%20title%3D%22%28%5B0-9%2C%5D%2B%29%22%3E&replace=%241&label=GHCR%20downloads&color=0969da&style=flat-square&cacheSeconds=300)](https://github.com/orgs/Low-Price-Hosting/packages/container/package/fedora) | [![fedora Docker Hub pulls](https://img.shields.io/docker/pulls/lphllc/fedora?label=Docker%20pulls&style=flat-square)](https://hub.docker.com/r/lphllc/fedora) | [![fedora Quay architectures](https://img.shields.io/badge/dynamic/json?url=https%3A%2F%2Fquay.io%2Fapi%2Fv1%2Frepository%2Flowpricehosting%2Ffedora%2Ftag%2F%3FspecificTag%3Dlatest%26onlyActiveTags%3Dtrue&query=%24.tags%5B0%5D.child_manifest_count&label=Quay%20architectures&color=ee0000&style=flat-square&cacheSeconds=300)](https://quay.io/repository/lowpricehosting/fedora?tab=tags) |
| [AlmaLinux](https://github.com/Low-Price-Hosting/AlmaLinux) | [![almalinux के GHCR डाउनलोड की संख्या](https://img.shields.io/badge/dynamic/regex?url=https%3A%2F%2Fgithub.com%2Forgs%2FLow-Price-Hosting%2Fpackages%2Fcontainer%2Fpackage%2Falmalinux&search=Total%20downloads%3C%2Fspan%3E%5Cs%2A%3Ch3%20title%3D%22%28%5B0-9%2C%5D%2B%29%22%3E&replace=%241&label=GHCR%20downloads&color=0969da&style=flat-square&cacheSeconds=300)](https://github.com/orgs/Low-Price-Hosting/packages/container/package/almalinux) | [![almalinux Docker Hub pulls](https://img.shields.io/docker/pulls/lphllc/almalinux?label=Docker%20pulls&style=flat-square)](https://hub.docker.com/r/lphllc/almalinux) | [![almalinux Quay architectures](https://img.shields.io/badge/dynamic/json?url=https%3A%2F%2Fquay.io%2Fapi%2Fv1%2Frepository%2Flowpricehosting%2Falmalinux%2Ftag%2F%3FspecificTag%3Dlatest%26onlyActiveTags%3Dtrue&query=%24.tags%5B0%5D.child_manifest_count&label=Quay%20architectures&color=ee0000&style=flat-square&cacheSeconds=300)](https://quay.io/repository/lowpricehosting/almalinux?tab=tags) |
| [Arch Linux](https://github.com/Low-Price-Hosting/ArchLinux) | [![archlinux के GHCR डाउनलोड की संख्या](https://img.shields.io/badge/dynamic/regex?url=https%3A%2F%2Fgithub.com%2Forgs%2FLow-Price-Hosting%2Fpackages%2Fcontainer%2Fpackage%2Farchlinux&search=Total%20downloads%3C%2Fspan%3E%5Cs%2A%3Ch3%20title%3D%22%28%5B0-9%2C%5D%2B%29%22%3E&replace=%241&label=GHCR%20downloads&color=0969da&style=flat-square&cacheSeconds=300)](https://github.com/orgs/Low-Price-Hosting/packages/container/package/archlinux) | [![archlinux Docker Hub pulls](https://img.shields.io/docker/pulls/lphllc/archlinux?label=Docker%20pulls&style=flat-square)](https://hub.docker.com/r/lphllc/archlinux) | [![archlinux Quay architectures](https://img.shields.io/badge/dynamic/json?url=https%3A%2F%2Fquay.io%2Fapi%2Fv1%2Frepository%2Flowpricehosting%2Farchlinux%2Ftag%2F%3FspecificTag%3Dlatest%26onlyActiveTags%3Dtrue&query=%24.tags%5B0%5D.child_manifest_count&label=Quay%20architectures&color=ee0000&style=flat-square&cacheSeconds=300)](https://quay.io/repository/lowpricehosting/archlinux?tab=tags) |
| [Rocky Linux](https://github.com/Low-Price-Hosting/RockyLinux) | [![rockylinux के GHCR डाउनलोड की संख्या](https://img.shields.io/badge/dynamic/regex?url=https%3A%2F%2Fgithub.com%2Forgs%2FLow-Price-Hosting%2Fpackages%2Fcontainer%2Fpackage%2Frockylinux&search=Total%20downloads%3C%2Fspan%3E%5Cs%2A%3Ch3%20title%3D%22%28%5B0-9%2C%5D%2B%29%22%3E&replace=%241&label=GHCR%20downloads&color=0969da&style=flat-square&cacheSeconds=300)](https://github.com/orgs/Low-Price-Hosting/packages/container/package/rockylinux) | [![rockylinux Docker Hub pulls](https://img.shields.io/docker/pulls/lphllc/rockylinux?label=Docker%20pulls&style=flat-square)](https://hub.docker.com/r/lphllc/rockylinux) | [![rockylinux Quay architectures](https://img.shields.io/badge/dynamic/json?url=https%3A%2F%2Fquay.io%2Fapi%2Fv1%2Frepository%2Flowpricehosting%2Frockylinux%2Ftag%2F%3FspecificTag%3Dlatest%26onlyActiveTags%3Dtrue&query=%24.tags%5B0%5D.child_manifest_count&label=Quay%20architectures&color=ee0000&style=flat-square&cacheSeconds=300)](https://quay.io/repository/lowpricehosting/rockylinux?tab=tags) |

GHCR और Docker Hub के बैज कुल डाउनलोड दिखाते हैं; Quay का बैज `latest` टैग के आर्किटेक्चर की संख्या दिखाता है। टैग और आर्किटेक्चर देखने के लिए बैज पर क्लिक करें। हर रजिस्ट्री के काउंटर अलग हैं; कैश के कारण अपडेट देर से दिख सकते हैं।

```bash
docker pull ghcr.io/low-price-hosting/ubuntu:latest
docker pull docker.io/lphllc/ubuntu:latest
docker pull quay.io/lowpricehosting/ubuntu:latest
```

<a id="versions-and-architectures"></a>

## संस्करण और आर्किटेक्चर के संदर्भ

[8 अक्टूबर 2026 की खोज योजना](https://github.com/Low-Price-Hosting/Container/actions/runs/37741062225) से संस्करण और आर्किटेक्चर के संदर्भ। ये खोजे गए लक्ष्य हैं; प्रकाशित आर्किटेक्चर चुने गए टैग के **OS/Arch** फ़ील्ड या OCI इंडेक्स में जाँचें।

| वितरण | संस्करण | प्लेटफ़ॉर्म — `linux/` उपसर्ग के साथ |
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

आर्किटेक्चर का समूह संस्करण के अनुसार बदल सकता है।

किसी टैग के वास्तविक आर्किटेक्चर जाँचें:

```bash
docker buildx imagetools inspect ghcr.io/low-price-hosting/ubuntu:latest
docker buildx imagetools inspect --raw ghcr.io/low-price-hosting/ubuntu:latest
```

<a id="quick-start"></a>

## जल्दी शुरू करें

उदाहरणों में `latest` की जगह वह **प्रकाशित टैग** चुनें जिसे आप इस्तेमाल करना चाहते हैं। सार्वजनिक इमेज डाउनलोड करने के लिए GHCR में लॉगिन की ज़रूरत नहीं है।

### डाउनलोड करें और चलाएँ

```bash
docker pull ghcr.io/low-price-hosting/ubuntu:latest
docker run --rm -it ghcr.io/low-price-hosting/ubuntu:latest /bin/sh
```

Docker मल्टी-आर्किटेक्चर टैग से आपके कंप्यूटर के आर्किटेक्चर के अनुरूप इमेज चुनता है।

### आर्किटेक्चर चुनें

```bash
docker pull --platform linux/arm64 ghcr.io/low-price-hosting/ubuntu:latest

docker run --rm --platform linux/arm64 \
  ghcr.io/low-price-hosting/ubuntu:latest \
  /bin/sh -c 'cat /etc/os-release'
```

किसी अलग प्रोसेसर परिवार के लिए बनी इमेज चलाने के लिए उपयुक्त एमुलेशन चाहिए।

### डाइजेस्ट से तय करें

```bash
docker image inspect --format '{{json .RepoDigests}}' \
  ghcr.io/low-price-hosting/ubuntu:latest

# <digest> की जगह इमेज का SHA256 मान लिखें।
docker pull ghcr.io/low-price-hosting/ubuntu@sha256:<digest>
```

संस्करण टैग अपडेट हो सकते हैं; डाइजेस्ट उसी इमेज को दोबारा इस्तेमाल करने देता है।

### अपनी इमेज में इस्तेमाल करें

```dockerfile
FROM ghcr.io/low-price-hosting/ubuntu:latest

COPY app/ /opt/app/
WORKDIR /opt/app
CMD ["/bin/sh"]
```

<a id="run-builds"></a>

## बिल्ड शुरू करना

[कार्रवाइयाँ → बेस इमेज बिल्ड करें → वर्कफ़्लो चलाएँ](https://github.com/Low-Price-Hosting/Container/actions/workflows/build-base-images.yml):

| फ़ील्ड | उपयोग |
|---|---|
| `distribution` | `all` या किसी वितरण का नाम। |
| `version` | `all` या सटीक संस्करण, जैसे `24.04`, `trixie`, `stream10`, `rolling`। |
| `verify_only` | `true`: दोबारा बिल्ड और परीक्षण, कोई प्रकाशन नहीं। `false`: बदली हुई या मौजूद न होने वाली इमेज बिल्ड करें, परीक्षण करें और प्रकाशित करें। |

चुने गए संस्करण के सभी खोजे गए आर्किटेक्चर पर काम किया जाता है। GitHub CLI के साथ:

```bash
# सभी वितरणों की बदली हुई या मौजूद न होने वाली इमेज बिल्ड और प्रकाशित करें।
gh workflow run build-base-images.yml \
  --repo Low-Price-Hosting/Container --ref main \
  -f distribution=all -f version=all -f verify_only=false

# Fedora इमेज का केवल बिल्ड और परीक्षण करें।
gh workflow run build-base-images.yml \
  --repo Low-Price-Hosting/Container --ref main \
  -f distribution=Fedora -f version=all -f verify_only=true
```

ऊपर का बिल्ड बैज नवीनतम वर्कफ़्लो परिणाम दिखाता है; केवल सत्यापन करने वाला रन इमेज प्रकाशित नहीं करता।

<a id="oci-metadata"></a>

## टैग और इमेज की जानकारी

| संदर्भ | अर्थ |
|---|---|
| `ubuntu:24.04`, `debian:trixie`, `centos:stream10` | संबंधित संस्करण के परीक्षण किए गए आर्किटेक्चर वाला मल्टी-आर्किटेक्चर टैग। |
| `latest` और अन्य उपनाम | वितरण के संस्करण कैटलॉग के अनुसार तय किए गए टैग। |
| `<image>@sha256:<digest>` | इमेज की सामग्री का अपरिवर्तनीय संदर्भ। |

इमेज के स्रोत, संस्करण और निर्माण की जानकारी OCI मेटाडेटा में मिलती है:

```bash
docker image inspect --format '{{json .Config.Labels}}' \
  ghcr.io/low-price-hosting/ubuntu:latest
```

`org.opencontainers.image.source` स्रोत रेसिपी की रिपॉज़िटरी, `org.opencontainers.image.version` संस्करण और `io.low-price-hosting.build.source` निर्माण कोड बताता है। मल्टी-आर्किटेक्चर इंडेक्स और आर्किटेक्चर एनोटेशन `docker buildx imagetools inspect --raw` से पढ़े जा सकते हैं।
