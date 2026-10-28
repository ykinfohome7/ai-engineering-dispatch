#!/usr/bin/env bash
set -euo pipefail
# Единен вход: запазва старото име на командата, без втори Paperclip install метод.
if [[ $# -gt 0 ]]; then
  echo 'Usage: bash scripts/start-paperclip.sh (private Codespaces only)' >&2
  exit 2
fi
exec bash "$(dirname "$0")/../dispatcher/install.sh"
