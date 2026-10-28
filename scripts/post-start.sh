#!/usr/bin/env bash
set -euo pipefail
printf 'BGDB AI-EMDS workspace resumed.\n'
printf 'Codespaces is ephemeral: running KSSH/Paperclip processes DO NOT survive stop.\n'
printf 'Start Paperclip manually: bash scripts/start-paperclip.sh\n'
printf 'For 24/7 hosting move Paperclip and KSSH gateway to always-on Proxmox VM.\n'
