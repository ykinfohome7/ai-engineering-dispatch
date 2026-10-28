#!/usr/bin/env bash
set -euo pipefail
# Проверява готовността, без да показва стойности на токени.
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"
failures=0
check() {
  if command -v "$2" >/dev/null 2>&1; then
    printf 'OK      %s\n' "$1"
  else
    printf 'MISSING %s\n' "$1"
    failures=$((failures + 1))
  fi
}
check 'Node.js' node
if command -v node >/dev/null 2>&1; then
  if node -e 'const [major,minor]=process.versions.node.split(".").map(Number);process.exit(major>24||(major===24&&minor>=11)?0:1)'; then
    echo 'OK      Node.js >=24.11'
  else
    echo 'MISSING Node.js >=24.11'
    failures=$((failures + 1))
  fi
fi
check pnpm pnpm
check python3 python3
check 'GitHub CLI (gh)' gh
check git git
if [[ -f dispatcher/paperclip/package.json ]]; then
  echo 'OK      Paperclip submodule initialized'
else
  echo 'MISSING Paperclip submodule; run git submodule update --init --recursive'
  failures=$((failures + 1))
fi
# Извежда само SET/MISSING; никога не отпечатва реални тайни.
for variable in PAPERCLIP_BASE_URL PAPERCLIP_COMPANY_ID PAPERCLIP_TOKEN OPENAI_API_KEY ANTHROPIC_API_KEY GITHUB_TOKEN SSH_CONNECTOR_TOKEN TAILSCALE_AUTHKEY PROXMOX_API_TOKEN; do
  if [[ -n "$(printenv "$variable" 2>/dev/null)" ]]; then
    printf 'SET     %s\n' "$variable"
  else
    printf 'MISSING %s (optional until needed)\n' "$variable"
  fi
done
if command -v python3 >/dev/null 2>&1; then
  if python3 - <<'PYCHECK'
import socket
# Проверява само локалния TCP порт.
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
    sock.bind(('127.0.0.1', 3100))
PYCHECK
  then
    echo 'OK      Port 3100 free'
  else
    echo 'MISSING Port 3100 occupied (Paperclip may already be running)'
    failures=$((failures + 1))
  fi
fi
printf 'Doctor: %s prerequisite issue(s).\n' "$failures"
[[ "$failures" -eq 0 ]]
