# BGDB AI-EMDS Roadmap

> 🇧🇬 Етапи: Codespaces, Proxmox и продукционна готовност.

## Phase 1 — Codespaces

> 🇧🇬 Файловете са създадени, но реалните агенти още не са активирани.

- [x] GitHub repository, GPL-3.0, roles, issue/PR templates, CI, devcontainer.
- [x] Python intake helper, tests and Paperclip upstream submodule.
- [x] Example agent registry, approvals, budgets, GPT action schema, documentation.
- [x] Integrations, label workflows, monitoring and release workflow examples.
- [ ] Register Claude Code/Codex agents and verify Paperclip assignments.
- [ ] Enforce individual budgets and human approvals in the running system.
- [ ] Implement authenticated, idempotent Issue ↔ Paperclip synchronization.

## Phase 2 — Proxmox

> 🇧🇬 Осигури постоянна работа, резервни копия и защитен достъп.

- [x] Example PostgreSQL Compose, Debian 12 LXC commands and Tailscale policy.
- [ ] Provision approved private persistent hosts and database storage.
- [ ] Deploy KSSH/Tailscale with tested restart recovery.
- [ ] Schedule encrypted backups, verify restore and enable monitoring.

## Phase 3 — Production

> 🇧🇬 Внедряването изисква независима проверка и план за връщане.

- [ ] Enable and verify GitHub required review/rulesets and CI gates.
- [ ] Complete security threat review, audit/incident runbooks and budgets.
- [ ] Run backup recovery, performance and resilience tests.
- [ ] Approve production release and rollback process.

See the current status in [docs/INVENTORY.md](docs/INVENTORY.md). A checked repository artifact is **not** proof of a deployed service.
