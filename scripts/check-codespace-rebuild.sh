#!/usr/bin/env bash
set -euo pipefail
# Само диагностика; не изписвай ключове, IP адреси или променливи на средата.
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
issues=0
report() {
  printf '%-9s %s\n' "$1" "$2"
  if [[ "$1" == MISSING || "$1" == RISK ]]; then
    issues=$((issues + 1))
  fi
}
if [[ -d "$ROOT/.git" ]]; then report OK "AI-EMDS checkout"; else report MISSING "AI-EMDS checkout"; fi
if [[ -r "$ROOT/dispatcher/paperclip/package.json" ]]; then report OK "Paperclip submodule"; else report MISSING "Paperclip submodule"; fi
if command -v node >/dev/null 2>&1; then report OK "Node.js"; else report MISSING "Node.js"; fi
if command -v python3 >/dev/null 2>&1; then report OK "Python"; else report MISSING "Python"; fi
if command -v ss >/dev/null 2>&1; then
  if ss -ltn | grep -Eq ':2222([[:space:]]|$)'; then report OK "SSH port 2222"; else report MISSING "SSH port 2222"; fi
else
  report MISSING "ss (iproute2)"
fi
if command -v curl >/dev/null 2>&1 && curl -fsS --max-time 5 http://127.0.0.1:3100/api/health >/dev/null 2>&1; then
  report OK "Paperclip health 3100"
else
  report MISSING "Paperclip health 3100"
fi
if [[ -r /home/bgadmin/.paperclip-worktrees/instances/bgdb-ai-emds/db/PG_VERSION ]]; then
  report OK "Local Paperclip database"
else
  report MISSING "Local Paperclip database"
fi
# Данните в /home/bgadmin може да се загубят при пълен Rebuild.
report RISK "Codespace Rebuild persistence unverified for /home/bgadmin"
printf 'RESULT: %s attention item(s); no files changed.\n' "$issues"
if ((issues)); then exit 2; fi
