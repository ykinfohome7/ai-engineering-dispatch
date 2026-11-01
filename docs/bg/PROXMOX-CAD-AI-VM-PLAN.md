# Plan: Windows 11 CAD + Debian 13 AI-EMDS on Proxmox (2026-11-01)

Status: **planning, not deployed**. This file is on a feature branch; do not merge until reviewed.

## Goal
- VM 210 `BGDB-CAD-WIN11`: Windows 11 x64, SOLIDWORKS, later SOLIDWORKS MCP.
- VM 220 `BGDB-AI-MANAGER`: always-on Debian 13 VM hosting the existing BGDB AI-EMDS repository `ykinfohome7/ai-engineering-dispatch`, Paperclip control plane and approved AI agent adapters.

## Important constraints from the existing Proxmox node
- VM 200 Windows Server 2025 is the only AD Domain Controller; preserve its disks, EFI/TPM, networking and backups.
- SanDisk Ultra 3D 2 TB (/dev/sdc, serial 2422SMD00523) is attached **directly to VM 200** as drive F: (temp/cache/pagefile); it is **not free Proxmox storage**.
- WD-VM200 is a 1 TB physical HDD with a thin-provisioned ~1.82 TiB VM 200 system disk; new workloads here could exhaust the host filesystem as VM 200 grows. Use a **new dedicated SSD/NVMe storage** for CAD and AI, or explicitly accept temporary slow HDD staging after checking real capacity.
- Samsung 2 TB contains `SAM-BACKUP` and CA/VM backups; it is **backup storage**, not the preferred production VM disk.
- Proxmox OS is on the PNY SSD; do not format any existing physical disks.
- KSSH remote connection was unavailable during preparation. No host changes were made.

## VM profiles (targets subject to host CPU/RAM audit)

| Item | VM 210 Windows CAD | VM 220 Debian AI |
|---|---|---|
| vCPU | 8 cores | 4 cores |
| RAM | 32768 MiB | 12288 MiB |
| Disk | 250 GiB on dedicated SSD | 100 GiB on dedicated SSD |
| CPU | host (no cross-generation live migration) | host |
| Machine | q35 | q35 |
| Firmware | OVMF + EFI | OVMF + EFI |
| TPM | v2.0 | not needed |
| Storage controller | VirtIO SCSI single | VirtIO SCSI single |
| Network | vmbr0, restrict access | vmbr1, private server VLAN |
| On boot | disabled until ready | enabled after installation |
| QEMU guest agent | install after OS | qemu-guest-agent |
| GPU | passthrough after PCI/IOMMU/certified-card review | not needed for control plane |

SOLIDWORKS recommends 32 GB RAM, SSD and certified graphics. Proxmox is not an explicitly supported SOLIDWORKS hypervisor. Validate licensing, compatibility, GPU and remote-session needs before production CAD.

## Read-only host audit (Proxmox Shell)

```bash
echo '=== HOST / CPU / RAM ==='
pveversion
lscpu | grep -E 'Model name|CPU\(s\)|Virtualization:'
free -h
echo '=== EXISTING VMs / CONTAINERS ==='
qm list
pct list
echo '=== STORAGE ==='
pvesm status
pvesm config
df -hT /mnt/wd-vm200 /mnt/sam-backup /var/lib/vz 2>/dev/null
echo '=== ISO FILES ==='
find /var/lib/vz/template/iso -maxdepth 1 -type f -name '*.iso' -printf '%f %s bytes\n' 2>/dev/null
echo '=== NETWORK ==='
ip -br addr show vmbr0 vmbr1
echo '=== GPU / IOMMU ==='
lspci | grep -Ei 'vga|3d|display'
dmesg | grep -Ei 'DMAR|IOMMU|AMD-Vi' | tail -15
echo '=== VM 200 — READ ONLY ==='
qm config 200 | grep -E '^(name|bios|boot|scsi|sata|tpm|net|agent)'
```

Stop if IDs 210/220 already exist, or if a suitably backed-up storage with sufficient free space is not available. Do not create large disks on the PNY Proxmox OS volume.

## ISO prerequisites
- Windows 11 x64 ISO: https://www.microsoft.com/en-us/software-download/windows11
- Debian 13 stable amd64 netinst: https://www.debian.org/releases/stable/debian-installer/
- VirtIO guest driver ISO: https://fedorapeople.org/groups/virt/virtio-win/direct-downloads/stable-virtio/virtio-win.iso
Upload ISO images into an approved Proxmox ISO storage. Use the GUI or `pvesm` to confirm actual volume IDs before referencing.

## Installation sequence
1. Inventory host storage/RAM/CPU and confirm there is a new SSD-capable Proxmox storage volume. Do not take VM 200 offline.
2. Create VM 220 first; select Debian 13 ISO, q35/OVMF, 4 cores, 12GB RAM, 100GB SSD, VirtIO SCSI and private `vmbr1`; configure a non-root `bgadmin` with Ed25519 SSH, limited sudo and guest agent. Confirm network/DNS.
3. `git clone --recurse-submodules https://github.com/ykinfohome7/ai-engineering-dispatch.git /opt/bgdb/ai-engineering-dispatch` as an unprivileged service/deployment user (ensure correct ownership). Run `bash scripts/doctor.sh` and Python tests after installing documented Node >=24.11, pnpm and Python tooling.
4. Deploy a **proper production service** for Paperclip (do not treat the current `dispatcher/install.sh`, which executes `pnpm dev`, as production-ready). Set up its supported PostgreSQL persistence, local authentication, systemd supervision, backups and restore test. Keep port 3100 private/loopback. No credentials in Git.
5. Configure Tailscale with approved ACL, key-only SSH/KSSH access and auditing. No public Funnel, no root/password SSH. Wire approved Paperclip Claude Code/Codex adapters, hard budgets and human approval controls.
6. Create Windows VM 210 with Windows 11 ISO, 250GB SSD, q35/OVMF/EFI/TPM 2.0, VirtIO driver ISO, guest tools, 8 CPU/32GB RAM. Install Windows; validate activation, GPU passthrough and graphics acceleration before SOLIDWORKS and MCP. Auto-start off.
7. Integrate via GitHub Issues → Paperclip (the current Issue ↔ Paperclip bridge is **not implemented**), branch/PR/CI and human-approved merge; CAD work is dispatched to the Windows VM through a separately authenticated worker.

## Security / data
- Repository is public; never commit secrets, client CAD models or private conversations.
- GitHub Issues and an explicit ChatGPT intake are the task handoff. The runtime cannot automatically ingest all prior or future ChatGPT chats without an authorized integration.
- Back up VM 220 and PostgreSQL daily to approved non-production storage; carry out an isolated restore drill. Back up CAD models separately from the VM.
- No changes to AD/DNS, VM 200, its SanDisk F:, or live Proxmox networking as part of this plan.
