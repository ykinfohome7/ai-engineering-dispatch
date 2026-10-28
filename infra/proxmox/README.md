# Proxmox production deployment — phase 2

> 🇧🇬 Този етап е планиран, не е инсталиран от настоящия commit.

## Migration checklist

> 🇧🇬 Изискват се постоянна VM/LXC, защитен достъп и тест за възстановяване.

- [ ] Provision dedicated Debian 13 VM/LXC, CPU/RAM/storage sizing, patch policy and a separate service account.
- [ ] Pin Paperclip release/submodule SHA; use tested Node 24.11+ and pnpm 9.15.4.
- [ ] Deploy persistent external PostgreSQL with access controls; plan encrypted backups, tested restore and disaster recovery.
- [ ] Join Tailnet; configure ACLs, least-privilege SSH and private KSSH gateway; disable root/password SSH once key access is verified.
- [ ] Use systemd services, readiness/liveness probes, startup ordering and restart policy.
- [ ] Configure Paperclip company, agents, budgets and approval workflows; enable audit logging.
- [ ] Validate API TLS and auth, rotate secrets safely, run CI/smoke tests, set rollback and maintenance window.
- [ ] Prove operation remains online independently of GitHub Codespaces.

## Scope and safety

> 🇧🇬 Не променяй съществуващи Proxmox VM и продукционна мрежа без одобрение.

The build scripts in this repository do not create, stop or modify any Proxmox VM/LXC. KSSH requires a separate approved deployment and credentials; never store them here.
