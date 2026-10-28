#!/usr/bin/env bash
set -euo pipefail
# Извежда отворените задачи и PR за всеки агент чрез GitHub CLI.
command -v gh >/dev/null || { echo 'GitHub CLI (gh) is required' >&2; exit 1; }
REPO='ykinfohome7/ai-engineering-dispatch'
gh auth status >/dev/null 2>&1 || { echo 'Sign in with gh before running this report' >&2; exit 1; }
labels=(agent:architect agent:developer agent:codex agent:reviewer agent:qa agent:devops agent:docs)
for label in "${labels[@]}"; do
  printf '\n### %s ###\n' "$label"
  echo 'Open Issues:'
  # Показва само метаданни, без да изпълнява съдържание от Issue.
  gh issue list -R "$REPO" --state open --label "$label" --limit 100 \
    --json number,title,url --jq '.[] | "#\(.number) \(.title) \(.url)"'
  echo 'Open Pull Requests:'
  gh pr list -R "$REPO" --state open --label "$label" --limit 100 \
    --json number,title,url --jq '.[] | "#\(.number) \(.title) \(.url)"'
done
