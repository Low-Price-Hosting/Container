#!/usr/bin/env bash
# Shared mirror checkout, tagging, and publishing functions.
# Keep an immutable tag per source revision (and, where needed, RPM
# repository metadata). Moving aliases update without rebuilding.
publish() {
  local version=$1 revision=$2 context=$3 dockerfile=$4
  shift 4
  local content_key=${BUILD_CONTENT_KEY:-$revision}
  local immutable="${version}-sha${content_key:0:12}"
  if ! docker buildx imagetools inspect "$image:$immutable" >/dev/null 2>&1; then
    docker buildx build --progress=plain --platform linux/amd64 \
      --label "org.opencontainers.image.source=$source_label" \
      --label "org.opencontainers.image.url=$source_label" \
      --label "org.opencontainers.image.revision=$revision" \
      --file "$dockerfile" --tag "$image:$immutable" \
      "${BUILD_ARGS[@]}" --push "$context"
  else
    echo "$image:$immutable already exists; skipping build."
  fi
  if [[ "$DISTRIBUTION" == Centos ]]; then
    docker run --rm "$image:$immutable" /bin/bash -c \
      'grep -qi centos /etc/os-release && command -v yum'
  fi
  local alias
  for alias in "$version" "$@"; do
    docker buildx imagetools create --tag "$image:$alias" "$image:$immutable"
  done
  # Each matrix job has its own runner; release build cache between versions.
  docker buildx prune --all --force
}
publish_alias() {
  local alias=$1 source=$2
  docker buildx imagetools create --tag "$image:$alias" "$image:$source"
}

clone_branch() {
  local branch=$1 sparse=${2:-}
  rm -rf source
  git clone --quiet --depth=1 --filter=blob:none --single-branch \
    --branch "$branch" --sparse "$mirror" source
  if [[ -n "$sparse" ]]; then
    git -C source sparse-checkout set "$sparse"
  else
    git -C source sparse-checkout disable
  fi
}

branches() {
  git ls-remote --heads "$mirror" | sed 's#.*refs/heads/##'
}
