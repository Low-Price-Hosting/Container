#!/usr/bin/env bash
# Run through build-base.sh so shared image settings are available.
curl -fsSL --retry 3 \
  https://raw.githubusercontent.com/docker-library/official-images/master/library/fedora \
  -o fedora-library
mapfile -t releases < <(awk '/^Tags: / {
  count = split(substr($0, 7), tags, ",")
  for (i = 1; i <= count; i++) {
    gsub(/^ +| +$/, "", tags[i])
    if (tags[i] ~ /^[0-9]+$/) print tags[i]
  }
}' fedora-library | sort -nu)
((${#releases[@]}))
latest_release=$(awk '/^Tags: / && /(^|, )latest(,|$)/ {
  count = split(substr($0, 7), tags, ",")
  for (i = 1; i <= count; i++) {
    gsub(/^ +| +$/, "", tags[i])
    if (tags[i] ~ /^[0-9]+$/) print tags[i]
  }
}' fedora-library)
[[ -n "$latest_release" ]]
for branch in "${releases[@]}"; do
  clone_branch "official-images/$branch" x86_64
  [[ -f source/x86_64/Dockerfile ]]
  revision=$(git -C source rev-parse HEAD)
  publish "$branch" "$revision" source/x86_64 source/x86_64/Dockerfile
done
publish_alias latest "$latest_release"
