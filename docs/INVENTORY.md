# Inventory snapshot — 2026-10-28

> 🇧🇬 Статусите са от провереното хранилище и кода, не доказателство за работеща инсталация.

## Available in repository

> 🇧🇬 Наличните файлове и функции са реални, но не са настроени агенти.

- [x] Public GitHub repo `ykinfohome7/ai-engineering-dispatch` on `main`, GPL-3.0 and original `.gitignore`/`LICENSE` preserved.
- [x] Python intake CLI (`roles`, `plan`, `submit` with `--execute`, `doctor`, `list`, `get`) plus local tests.
- [x] Codespaces devcontainer, CI, agent runbooks, task/bug Issue templates, PR template, CODEOWNERS and environment template.
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

- [x] `AGENTS.md`, `CONTRIBUTING.md`, `SECURITY.md`, architecture, inventory, security, operations guides, plus full `docs/bg/` documentation and community notices.
- [x] Issue and PR templates, CODEOWNERS and CI with Python tests and basic leaked-secret pattern check.
- [ ] Branch protection/ruleset activated in GitHub (not changed by this commit).
- [ ] GitHub Issue-to-Paperclip sync implemented; currently manual linking.
- [ ] Confirm GitHub Actions CI for the newest commit after GitHub runs it.

## Open-source and operational readiness

> 🇧🇬 Проектните файлове са налични, но реалните услуги трябва да бъдат конфигурирани.

- [x] Repository, GPL-3.0 LICENSE, CODE_OF_CONDUCT, CHANGELOG, VERSION and MIT third-party notice.
- [x] GitHub CI, Issue/PR templates, CODEOWNERS, Dependabot, Paperclip update PR workflow.
- [x] Devcontainer, upstream Paperclip git submodule and full Bulgarian guides.
- [ ] Real Claude Code/Codex agents registered and authenticated in Paperclip.
- [ ] Per-agent budgets, cost ceilings and human approval gates configured and tested.
- [ ] Tailscale/KSSH session and restart recovery tested on an always-on host.
- [ ] Proxmox persistent deployment, backups and restore drill completed.
- [ ] Centralized logs, uptime monitoring, alerts and incident response tested.
- [ ] Main branch rulesets / required reviewer and CI checks enabled in repository settings.
- [ ] GitHub Actions PR creation permissions enabled for the Paperclip update workflow.
