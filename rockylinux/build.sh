#!/usr/bin/env bash
# Run through build-base.sh so shared image settings are available.
mapfile -t releases < <(branches | grep -E '^Rocky-[0-9]+\.[0-9]+\.[0-9]+-Base-x86_64$' | sort -V)
((${#releases[@]}))
declare -A newest=()
for branch in "${releases[@]}"; do
  major=${branch#Rocky-}; major=${major%%.*}
  newest[$major]=$branch
done
for major in "${!newest[@]}"; do
  branch=${newest[$major]}
  clone_branch "$branch"
  [[ -f source/Dockerfile ]]
  revision=$(git -C source rev-parse HEAD)
  full=${branch#Rocky-}; full=${full%-Base-x86_64}
  minor=${full%.*}
  publish "$full" "$revision" source source/Dockerfile "$minor" "$major"
done
latest_major=$(printf '%s\n' "${!newest[@]}" | sort -n | tail -n 1)
publish_alias latest "$latest_major"
