#!/usr/bin/env bash
# Run through build-base.sh so shared image settings are available.
clone_branch releases
revision=$(git -C source rev-parse HEAD)
version=$(sed -n 's/^LABEL org.opencontainers.image.version="\([^"]*\)"/\1/p' source/Dockerfile.base | head -n 1)
[[ -n "$version" ]]
publish "$version" "$revision" source source/Dockerfile.base latest base
