#!/usr/bin/env bash
set -euo pipefail
python3 scripts/generate-build-workflow.py
git add -- .github/workflows/build-base-images.yml scripts/release-jobs.json
if ! git diff --cached --quiet; then
  identity=$(gh api user)
  login=$(jq -er .login <<< "$identity")
  account_id=$(jq -er .id <<< "$identity")
  git config user.name "$login"
  git config user.email "$account_id+$login@users.noreply.github.com"
  git commit -m 'Update automatically discovered release jobs'
  git push origin HEAD:main
fi
gh workflow run build-base-images.yml --ref main \
  -f "distribution=${SELECTED:-all}" -f version=all -f verify_only=false
