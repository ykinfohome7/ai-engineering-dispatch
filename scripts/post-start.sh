#!/usr/bin/env bash
set -euo pipefail
# Преустановен Codespace не може сам да се събуди; това се пуска след възобновяване.
printf 'BGDB AI-EMDS Codespace resumed; processes may need manual restart.
'
printf 'Run: bash dispatcher/install.sh (Paperclip, private port 3100)
'
printf 'For 24/7 KSSH/Tailscale/Paperclip, deploy to Proxmox.
'
