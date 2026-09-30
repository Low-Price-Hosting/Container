#!/usr/bin/env bash
# Run through build-base.sh so shared image settings are available.
mapfile -t releases < <(branches | grep -E '^[0-9]+$' | sort -n)
((${#releases[@]}))
for branch in "${releases[@]}"; do
  clone_branch "$branch" default/amd64
  [[ -f source/default/amd64/Dockerfile ]] || continue
  revision=$(git -C source rev-parse HEAD)
  mapfile -t aliases < <(sed -n 's/^# Tags: //p' source/default/amd64/Dockerfile | head -n 1 | tr ',' '\n' | xargs -n1)
  ((${#aliases[@]}))
  publish "$branch" "$revision" source/default/amd64 source/default/amd64/Dockerfile "${aliases[@]}"
done
