#!/usr/bin/env bash
# Run through build-base.sh so shared image settings are available.
git clone --quiet --depth=1 --filter=blob:none --single-branch \
  --branch dist-amd64 --sparse "$mirror" source
mapfile -t suites < source/suites
for suite in "${suites[@]}"; do
  case "$suite" in experimental|rc-buggy) continue;; esac
  clone_branch dist-amd64 "$suite"
  [[ -f "source/$suite/Dockerfile" ]] || continue
  revision=$(git -C source rev-parse HEAD)
  aliases=()
  [[ "$suite" == stable ]] && aliases+=(latest)
  publish "$suite" "$revision" "source/$suite" "source/$suite/Dockerfile" "${aliases[@]}"
done
