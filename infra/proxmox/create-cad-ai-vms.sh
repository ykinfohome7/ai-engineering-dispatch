#!/usr/bin/env bash
# BGDB: create Windows 11 CAD VM 210 and Debian 13 AI Manager VM 220.
# Dry-run by default. Requires explicit --apply, ISO paths, approved images storage.
# This script does NOT start VMs, touch VM 200, repartition disks, or install guest OSes.
set -Eeuo pipefail

WIN_ID=210
AI_ID=220
WIN_NAME=BGDB-CAD-WIN11
AI_NAME=BGDB-AI-MANAGER

STORAGE="${BGDB_VM_STORAGE:-}"
WIN_ISO="${BGDB_WIN11_ISO:-}"
DEBIAN_ISO="${BGDB_DEBIAN13_ISO:-}"
VIRTIO_ISO="${BGDB_VIRTIO_ISO:-}"
EFI_STORAGE="${BGDB_EFI_STORAGE:-local-lvm}"
WIN_RAM="${BGDB_WIN_RAM_MB:-32768}"
AI_RAM="${BGDB_AI_RAM_MB:-12288}"

die() { printf 'STOP: %s\n' "$*" >&2; exit 1; }

[[ "${1:-}" == "" || "${1:-}" == "--apply" ]] || die "Usage: bash $0 [--apply]"
printf '=== Planned VMs (not started automatically) ===\n'
printf 'VM %s: %s, Win11, 8 vCPU, %s MiB RAM, 250 GiB, vmbr0\n' "$WIN_ID" "$WIN_NAME" "$WIN_RAM"
printf 'VM %s: %s, Debian13, 4 vCPU, %s MiB RAM, 100 GiB, vmbr1\n' "$AI_ID" "$AI_NAME" "$AI_RAM"
printf 'Images storage: %s\n' "${STORAGE:-NOT SET}"
printf 'EFI/TPM storage: %s\n' "$EFI_STORAGE"
printf 'Win11 ISO: %s\nDebian ISO: %s\nVirtIO ISO: %s\n' "${WIN_ISO:-NOT SET}" "${DEBIAN_ISO:-NOT SET}" "${VIRTIO_ISO:-NOT SET}"
printf 'NOTE: /dev/sdc (SanDisk, serial 2422SMD00523) belongs to VM 200 F:, never use it here.\n'

if [[ "${1:-}" != "--apply" ]]; then
  printf '\nDRY RUN ONLY. Read docs/bg/PROXMOX-CAD-AI-VM-PLAN.md before --apply.\n'
  exit 0
fi

[[ "${BGDB_HUMAN_APPROVED:-}" == YES ]] || die "Set BGDB_HUMAN_APPROVED=YES only after reviewing plan"
(( EUID == 0 )) || die "Run as root on approved Proxmox node"
for command in qm pct pvesm ip mountpoint awk; do command -v "$command" >/dev/null || die "Missing $command"; done
[[ "$STORAGE" != "" && "$WIN_ISO" != "" && "$DEBIAN_ISO" != "" && "$VIRTIO_ISO" != "" ]] || die "Set BGDB_VM_STORAGE, BGDB_WIN11_ISO, BGDB_DEBIAN13_ISO and BGDB_VIRTIO_ISO"

case "$STORAGE" in
  SAM-BACKUP|SANDISK-VM|local-lvm) die "Storage $STORAGE is reserved for backups, VM 200 passthrough, or Proxmox OS";;
  WD-VM200)
    [[ "${BGDB_ALLOW_HDD:-}" == YES ]] || die "WD HDD holds VM 200 thin-provisioned boot disk. Require BGDB_ALLOW_HDD=YES for intentional temporary staging";;
esac
[[ "$STORAGE" != "$EFI_STORAGE" ]] || die "EFI storage must be separate from VM images storage for this profile"

for id in "$WIN_ID" "$AI_ID"; do
  if qm config "$id" >/dev/null 2>&1 || pct config "$id" >/dev/null 2>&1; then
    die "ID $id is already used by a VM or CT"
  fi
done

for bridge in vmbr0 vmbr1; do
  ip link show "$bridge" >/dev/null 2>&1 || die "Bridge $bridge not present"
done

for iso in "$WIN_ISO" "$DEBIAN_ISO" "$VIRTIO_ISO"; do
  [[ "$iso" == *:iso/*.iso ]] || die "ISO volume ID expected: storage:iso/name.iso, got $iso"
  iso_path="$(pvesm path "$iso")" || die "Cannot resolve ISO $iso"
  [[ -r "$iso_path" ]] || die "ISO not readable: $iso_path"
done

for st in "$STORAGE" "$EFI_STORAGE"; do
  st_state="$(pvesm status | awk -v n="$st" '$1==n {print $3}')"
  [[ "$st_state" == active ]] || die "Storage $st is not active"
  st_conf="$(pvesm config "$st")" || die "Storage $st is not configured"
  grep -Eq '^[[:space:]]*content[[:space:]]+.*images' <<< "$st_conf" || die "Storage $st does not allow VM images"
done

# Directory storage must be mounted at the configured path; otherwise a
# missing mount can silently fill the Proxmox OS root filesystem.
if [[ "$STORAGE" == WD-VM200 ]]; then
  mountpoint -q /mnt/wd-vm200 || die "WD-VM200 filesystem not mounted"
fi

# Need enough unallocated physical space for planned guests, plus reserve.
# Even on thin storage this does not guarantee room for VM 200 future growth.
free_kb="$(pvesm status | awk -v n="$STORAGE" '$1==n {print $6}')"
[[ "$free_kb" =~ ^[0-9]+$ ]] || die "Cannot read free space for $STORAGE"
(( free_kb >= 450 * 1024 * 1024 )) || die "Need >=450 GiB free on $STORAGE (350 GiB guests + 100 GiB reserve)"
if [[ "$STORAGE" == WD-VM200 ]]; then
  printf 'WARNING: thin-provisioned VM 200 can expand beyond WD capacity. Monitor storage continuously.\n'
fi

[[ "$WIN_RAM" =~ ^[0-9]+$ && "$AI_RAM" =~ ^[0-9]+$ ]] || die "Memory values must be MiB integers"
printf '\n=== LAST CONFIRMATION ===\n'
read -r -p 'Type CREATE-BGDB-210-220: ' confirmation
[[ "$confirmation" == CREATE-BGDB-210-220 ]] || die "Cancelled"

echo '=== Creating Debian 13 AI manager VM 220 (powered off) ==='
qm create "$AI_ID" --name "$AI_NAME" --machine q35 --bios ovmf \
  --ostype l26 --cpu host --sockets 1 --cores 4 --memory "$AI_RAM" \
  --scsihw virtio-scsi-single --agent enabled=1 --onboot 0 \
  --net0 virtio,bridge=vmbr1,firewall=1
qm set "$AI_ID" --efidisk0 "$EFI_STORAGE:1,efitype=4m,pre-enrolled-keys=1"
qm set "$AI_ID" --scsi0 "$STORAGE:100"
qm set "$AI_ID" --ide2 "$DEBIAN_ISO,media=cdrom"
qm set "$AI_ID" --boot 'order=ide2;scsi0'

echo '=== Creating Windows 11 CAD VM 210 (powered off) ==='
qm create "$WIN_ID" --name "$WIN_NAME" --machine q35 --bios ovmf \
  --ostype win11 --cpu host --sockets 1 --cores 8 --memory "$WIN_RAM" \
  --scsihw virtio-scsi-single --agent enabled=1 --onboot 0 \
  --net0 virtio,bridge=vmbr0,firewall=1
qm set "$WIN_ID" --efidisk0 "$EFI_STORAGE:1,efitype=4m,pre-enrolled-keys=1"
qm set "$WIN_ID" --tpmstate0 "$EFI_STORAGE:1,version=v2.0"
qm set "$WIN_ID" --scsi0 "$STORAGE:250"
qm set "$WIN_ID" --ide2 "$WIN_ISO,media=cdrom"
qm set "$WIN_ID" --ide0 "$VIRTIO_ISO,media=cdrom"
qm set "$WIN_ID" --boot 'order=ide2;scsi0'

echo '=== Result: only empty VMs and uninstalled virtual disks created ==='
qm config "$AI_ID"
qm config "$WIN_ID"
echo 'NEXT: install guest OSes via Proxmox console. Never start both VMs before checking host RAM.'
