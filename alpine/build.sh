#!/usr/bin/env bash
# Run through build-base.sh so shared image settings are available.
curl -fsSL --retry 3 \
  https://raw.githubusercontent.com/docker-library/official-images/master/library/alpine \
  -o alpine-library
mapfile -t releases < <(awk '/^Tags: / {
  count = split(substr($0, 7), tags, ",")
  for (i = 1; i <= count; i++) {
    gsub(/^ +| +$/, "", tags[i])
    if (tags[i] ~ /^3\.[0-9]+$/) print "v" tags[i]
  }
}' alpine-library | sort -Vu)
((${#releases[@]}))
for branch in "${releases[@]}"; do
  clone_branch "$branch" x86_64
  [[ -f source/x86_64/Dockerfile ]] || continue
  version=$(cat source/VERSION)
  revision=$(git -C source rev-parse HEAD)
  minor=${version%.*}
  aliases=()
  [[ "$branch" == "${releases[-1]}" ]] && aliases+=(latest 3)
  publish "$version" "$revision" source/x86_64 source/x86_64/Dockerfile "$minor" "${aliases[@]}"
done
