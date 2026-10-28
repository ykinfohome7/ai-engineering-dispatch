# Tailscale private connectivity

> 🇧🇬 Вътрешната мрежа е само за упълномощени устройства и услуги.

## Policy

> 🇧🇬 Достъпът до сървърите минава през Tailscale ACL и KSSH.

Use Tailnet ACLs/grants, least-privilege device identity, short-lived auth keys and authenticated connections. Bind persistent MCP/KSSH gateway and Paperclip services to loopback/Tailnet interfaces, not unrestricted internet; never publish a Funnel endpoint as a workaround. KSSH Tailscale commands must inspect current state before editing and request human approval for network changes.

## Restart and recovery

> 🇧🇬 Спирането на Codespace спира и Tailscale/KSSH процесите вътре в него.

A stopped Codespace cannot run its own wakeup job. After manual resume, verify `tailscale status`, DNS, certificates, TCP reachability and KSSH health. For uninterrupted service move Tailscale and the MCP/KSSH gateway into an always-on Proxmox VM with automatic restart, health checks and backups.
