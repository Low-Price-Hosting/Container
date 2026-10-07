#!/usr/bin/env bash
set -euo pipefail

work=$(mktemp -d)
trap 'rm -rf -- "$work"' EXIT
gh auth setup-git
gh repo clone Low-Price-Hosting/Container "$work/Container" -- --quiet --depth=1 --branch=main
cd "$work/Container"
git config user.name "$(gh api user --jq .login)"
git config user.email "$(gh api user --jq '"\(.id)+\(.login)@users.noreply.github.com"')"

for attempt in 1 2 3; do
  git fetch --quiet origin main
  # This is a disposable clone owned by this script.
  git reset --quiet --hard origin/main
  python3 scripts/generate-release-workflow.py
  git diff --quiet -- .github/workflows/build-base-images.yml && exit 0
  git add .github/workflows/build-base-images.yml
  git commit -m 'Update automatically discovered release groups'
  if git push origin HEAD:main; then
    exit 0
  fi
  ((attempt < 3)) || exit 1
  sleep $((attempt * 2))
done
