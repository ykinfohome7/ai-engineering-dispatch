#!/usr/bin/env bash
set -euo pipefail
# Без --apply само показва командите; нищо не се създава автоматично.
: "${PVE_TEMPLATE:?Set an approved Debian 12 template volume ID}"
: "${PVE_STORAGE:?Set approved Proxmox storage ID}"
: "${PVE_BRIDGE:?Set approved private bridge name}"
: "${CTID_PAPERCLIP:?Set a free integer CTID}"
: "${CTID_POSTGRES:?Set a different free integer CTID}"
: "${SSH_PUBLIC_KEY_FILE:?Set an approved public SSH key file}"
[[ "$CTID_PAPERCLIP" =~ ^[0-9]+$ && "$CTID_POSTGRES" =~ ^[0-9]+$ ]] || {
  echo "CTIDs must be integers" >&2; exit 1;
}
[[ "$CTID_PAPERCLIP" != "$CTID_POSTGRES" ]] || { echo "CTIDs must differ" >&2; exit 1; }
[[ -f "$SSH_PUBLIC_KEY_FILE" ]] || { echo "Missing SSH public key file" >&2; exit 1; }
[[ "$PVE_TEMPLATE" == *debian-12* ]] || { echo "Require Debian 12 template" >&2; exit 1; }
# Създава непривилегировани LXC контейнери, без публични портове.
paperclip=(pct create "$CTID_PAPERCLIP" "$PVE_TEMPLATE" --hostname bgdb-paperclip
  --cores 2 --memory 4096 --rootfs "$PVE_STORAGE:16" --unprivileged 1 --onboot 1
  --net0 "name=eth0,bridge=$PVE_BRIDGE,ip=dhcp,firewall=1"
  --ssh-public-keys "$SSH_PUBLIC_KEY_FILE")
postgres=(pct create "$CTID_POSTGRES" "$PVE_TEMPLATE" --hostname bgdb-postgres
  --cores 2 --memory 4096 --rootfs "$PVE_STORAGE:32" --unprivileged 1 --onboot 1
  --net0 "name=eth0,bridge=$PVE_BRIDGE,ip=dhcp,firewall=1"
  --ssh-public-keys "$SSH_PUBLIC_KEY_FILE")
printf '%q ' "${paperclip[@]}"; printf '
'
printf '%q ' "${postgres[@]}"; printf '
'
# Изисква отделно човешко одобрение и проверка на целевите CTID.
if [[ "${1:-}" != "--apply" ]]; then
  echo 'Dry run only. Use --apply after explicit approval.'
  exit 0
fi
[[ "${BGDB_HUMAN_APPROVED:-}" == YES ]] || { echo "Human approval required" >&2; exit 1; }
command -v pct >/dev/null || { echo "Run on approved Proxmox host" >&2; exit 1; }
for id in "$CTID_PAPERCLIP" "$CTID_POSTGRES"; do
  ! pct status "$id" >/dev/null 2>&1 || { echo "Container $id exists; refusing overwrite" >&2; exit 1; }
done
"${paperclip[@]}"
"${postgres[@]}"
echo 'LXC containers created; Paperclip/Postgres must be installed separately.'
