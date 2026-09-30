ARG CENTOS_MAJOR
FROM quay.io/centos/centos:stream${CENTOS_MAJOR} AS builder
ARG CENTOS_MAJOR

COPY build-rootfs.sh /usr/local/bin/build-rootfs
COPY CentOS-Stream-*-container-*.ks /kickstarts/
RUN bash /usr/local/bin/build-rootfs "$CENTOS_MAJOR"

FROM scratch
COPY --from=builder /rootfs/ /
CMD ["/bin/bash"]
