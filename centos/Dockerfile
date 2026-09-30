ARG CENTOS_BUILDER
FROM ${CENTOS_BUILDER} AS builder
ARG CENTOS_MAJOR
ARG CENTOS_METADATA_KEY

COPY build-rootfs.sh /usr/local/bin/build-rootfs
COPY CentOS-Stream-*-container-*.ks /kickstarts/
RUN test -n "$CENTOS_METADATA_KEY" && bash /usr/local/bin/build-rootfs "$CENTOS_MAJOR"

FROM scratch
COPY --from=builder /rootfs/ /
CMD ["/bin/bash"]
