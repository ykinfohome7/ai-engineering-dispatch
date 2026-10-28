#!/usr/bin/env bash
set -euo pipefail
# Проверява средата и използва само посочения git submodule.
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"
command -v git >/dev/null || { echo 'git is required' >&2; exit 1; }
command -v node >/dev/null || { echo 'Node.js >= 24.11.0 is required' >&2; exit 1; }
node -e 'const [a,b]=process.versions.node.split(".").map(Number);if(a<24||(a===24&&b<11))process.exit(1)' || { echo 'Node.js >= 24.11.0 required' >&2; exit 1; }
# Ползва upstream pin-а, вместо глобален, потенциално несъвместим pnpm.
if ! command -v pnpm >/dev/null; then
  command -v corepack >/dev/null || { echo 'Install pnpm 9.15.4 or Corepack' >&2; exit 1; }
  corepack enable
fi
# Изтегля submodule-а на Paperclip; при неуспех прекратява без нови външни команди.
git submodule update --init --recursive
cd dispatcher/paperclip
[ -f package.json ] || { echo 'Paperclip submodule not initialized' >&2; exit 1; }
# Инсталира зависимостите със заключените версии за възпроизводим build.
pnpm install --frozen-lockfile
# Стартира UI + API (обичайно порт 3100); не прави публично споделяне.
export PAPERCLIP_TELEMETRY_DISABLED=1
exec pnpm dev
