#!/usr/bin/env bash
set -euo pipefail
mode="${1:-loopback}"
case "$mode" in loopback|tailnet) ;; *) echo 'Usage: scripts/start-paperclip.sh [loopback|tailnet]' >&2; exit 2 ;; esac
if ! command -v node >/dev/null || ! command -v npx >/dev/null; then
  echo 'Install Node.js >=24.11 and npm first.' >&2; exit 1
fi
node -e 'const v=process.versions.node.split(".").map(Number);if(v[0]<24||(v[0]===24&&v[1]<11))process.exit(1)' || { echo 'Node.js >=24.11 required' >&2; exit 1; }
export PAPERCLIP_TELEMETRY_DISABLED=1
export PAPERCLIP_NO_BROWSER=1
printf 'Starting upstream Paperclip in %s mode (private by default).\n' "$mode"
printf 'Keep API keys out of the repository. This process stops when Codespace stops.\n'
exec npx --yes paperclipai@latest onboard --yes --bind "$mode"
