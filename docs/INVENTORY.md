# Inventory snapshot — 2026-10-28

> 🇧🇬 Статусите са от провереното хранилище и кода, не доказателство за работеща инсталация.

## Available in repository

> 🇧🇬 Наличните файлове и функции са реални, но не са настроени агенти.

- [x] Public GitHub repo `ykinfohome7/ai-engineering-dispatch` on `main`, GPL-3.0 and original `.gitignore`/`LICENSE` preserved.
- [x] Python intake CLI (`roles`, `plan`, `submit` with `--execute`, `doctor`, `list`, `get`) plus local tests.
- [x] Codespaces definition, CI, agent runbooks, issue template, environment template.
- [x] Paperclip git submodule pinned to a known upstream commit, not a vendor copy.
- [ ] Requested `ykinfohome7/paperclip` fork accessible (404 at time of check).

## Agents

> 🇧🇬 Описани са седем роли; изпълнители и бюджетни ограничения предстоят.

- [x] Role documents: Architect, Claude Code Developer, Codex Developer 2, Reviewer, QA, DevOps, Docs.
- [x] Python role hints for all seven roles.
- [ ] Live Paperclip agent accounts/adapters registered and authenticated.
- [ ] Per-agent token/cost budgets, alerts and approval gates configured and verified.
- [ ] Automatic role-to-issue routing and independent review enforcement confirmed.

## Infrastructure

> 🇧🇬 Codespaces е временна среда; Proxmox е предвиденият постоянен сървър.

- [x] Paperclip local embedded PostgreSQL path documented, external database not required for phase 1.
- [x] Tailscale/KSSH security and Codespace restart restrictions documented.
- [ ] Paperclip installed and running on port 3100; actual UI access tested.
- [ ] Connected and healthy Tailscale/KSSH session.
- [ ] Proxmox VM/LXC, external PostgreSQL, systemd and backups installed/tested.

## Management and documentation

> 🇧🇬 Политиката и документацията са в Git; настройките в реалните услуги предстоят.

- [x] `AGENTS.md`, `CONTRIBUTING.md`, `SECURITY.md`, architecture, inventory, security and operations guides.
- [x] Issue and PR policy documented; CI includes tests and basic leaked-secret pattern check.
- [ ] Branch protection/ruleset activated in GitHub (not changed by this commit).
- [ ] GitHub Issue-to-Paperclip sync implemented; currently manual linking.
- [ ] Live CI run for this commit confirmed; run remains pending until GitHub finishes checks.
