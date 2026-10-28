# BGDB AI-EMDS — AI Engineering Management & Dispatch System

> 🇧🇬 Инженерен диспечер за GitHub Issues, Paperclip и AI агенти.

[![GPL-3.0](https://img.shields.io/badge/license-GPL--3.0-blue.svg)](LICENSE)
[![BGDB AI-EMDS CI](https://github.com/ykinfohome7/ai-engineering-dispatch/actions/workflows/ci.yml/badge.svg)](https://github.com/ykinfohome7/ai-engineering-dispatch/actions/workflows/ci.yml)
[![Version 0.3.0](https://img.shields.io/badge/version-0.2.0-informational.svg)](VERSION)

**Version:** [VERSION](VERSION) is the canonical version file (currently 0.3.0). **Maintainer:** BGDB.EU. **Български:** [Пълно ръководство](docs/bg/README.md).

**v0.3.0 (onboarding scaffold)** for `ykinfohome7/ai-engineering-dispatch`. ChatGPT/user supplies an engineering task, this lightweight CLI prepares and optionally creates a **Paperclip** issue, and Paperclip manages real AI agent assignment, budgets and approvals. Works first in a private GitHub Codespace; production target is an always-on Proxmox VM using Tailscale and KSSH.

> **Current status:** CLI and tests are implemented. Paperclip, agent adapters (Claude Code/Codex), Tailscale/KSSH and a persistent deployment **are not yet installed or connected by this repository**. No shell commands from task descriptions are executed.

**Start here:** [Quickstart (English)](docs/QUICKSTART.md) · [Бърз старт (БГ)](docs/bg/QUICKSTART.md) · [Doctor](scripts/doctor.sh) · [Agent registration](scripts/register-agents.py).

> 🇧🇬 Новото ръководство описва настройка от нулата, без автоматично включване на сървъри.

## Quickstart (Codespaces)

> 🇧🇬 Бързо стартиране в GitHub Codespaces; портът трябва да остане частен.

1. Open this repository in GitHub Codespaces. The devcontainer adds Python 3.12 and Node 24.
2. Run `bash scripts/bootstrap.sh` to test the CLI.
3. Run `bash scripts/start-paperclip.sh` to install/onboard and start Paperclip privately; create the company and AI agents in its UI.
4. Set environment values for the currently running shell (never put them in Git):

   ```bash
   export PAPERCLIP_BASE_URL='http://127.0.0.1:3100'
   export PAPERCLIP_COMPANY_ID='your-real-company-uuid'
   # For authenticated deployments also export PAPERCLIP_TOKEN using a scoped token.
   # To auto-assign to an existing Paperclip agent:
   # export PAPERCLIP_AGENT_DEVELOPER_ID='agent-uuid'
   ```

5. Plan a task (no network call):

   ```bash
   PYTHONPATH=src python3 -m bgdb_dispatch.cli roles
   PYTHONPATH=src python3 -m bgdb_dispatch.cli plan "Review KSSH security and reconnect logic" --role reviewer --priority high
   ```

6. Verify connection, then explicitly submit:

   ```bash
   PYTHONPATH=src python3 -m bgdb_dispatch.cli doctor
   PYTHONPATH=src python3 -m bgdb_dispatch.cli submit "Add KSSH reconnect tests" --role qa --priority high --execute
   PYTHONPATH=src python3 -m bgdb_dispatch.cli list
   ```

`submit` **without `--execute` is a dry run**. With no `PAPERCLIP_AGENT_<ROLE>_ID`, the task is created **unassigned**. Routing is keyword-based guidance, not a real AI manager model; actual agents and authorization are provided by Paperclip.

## Agent roles

> 🇧🇬 Всеки агент има отделна роля и независим контрол.

| Role | Responsibility | Agent option |
| --- | --- | --- |
| Architect | design, decomposition | Claude Code / Codex |
| Developer | implementation | Claude Code / Codex |
| Reviewer | architecture/security review | Claude Code / Codex + human |
| QA | automated tests, reproducibility | Claude Code / Codex |
| DevOps | build, environment, deploy | Claude Code / Codex; approval gate |
| Docs | documentation and runbooks | Claude Code / Codex |

## Security & uptime

> 🇧🇬 Без тайни в Git и без обещание за 24/7 работа от Codespaces.

Repository is **public**. Never commit any credentials. The CLI allows HTTP only on localhost and requires HTTPS + token for remote URLs. Keep Codespaces forwarded ports private. A Codespace automatically stops and cannot keep KSSH/Paperclip running 24/7; move the gateway and service to a Proxmox VM for persistent availability. See [Operations](docs/OPERATIONS.md) and [Architecture](docs/ARCHITECTURE.md).

**Upstream:** [Paperclip](https://github.com/paperclipai/paperclip) — use its documented [Issues API](https://github.com/paperclipai/paperclip/blob/master/docs/api/issues.md).

**License:** GPL-3.0 (existing repository license). Contributions welcome.

## Repository layout and community

> 🇧🇬 Документацията, управлението и инфраструктурата са отделени от външния Paperclip submodule.

| Path | Purpose |
| --- | --- |
| [AGENTS.md](AGENTS.md), [agents/](agents/) | Independent AI agent roles and rules |
| [src/bgdb_dispatch/](src/bgdb_dispatch/) | Python task intake helper |
| [dispatcher/](dispatcher/) | Paperclip launcher and pinned upstream submodule |
| [intake/chatgpt/](intake/chatgpt/) | ChatGPT → Issue → Paperclip workflow |
| [infra/](infra/) | PostgreSQL, Tailscale and Proxmox notes |
| [docs/](docs/) | Architecture, inventory, operations and security |
| [docs/bg/](docs/bg/) | Full Bulgarian project, architecture and agent guides |
| [.github/](.github/) | PR/Issue templates, CODEOWNERS, CI and updates |
| [VERSION](VERSION), [CHANGELOG.md](CHANGELOG.md) | Current version and changes |

**Community and licenses:** [Contributing](CONTRIBUTING.md) · [Code of Conduct](CODE_OF_CONDUCT.md) · [Changelog](CHANGELOG.md) · [Third-party notices](THIRD_PARTY_NOTICES.md) · [Security](SECURITY.md) · [Bulgarian guides](docs/bg/README.md). This repository remains GPL-3.0; Paperclip remains MIT. Keep the version badge synchronized with the canonical VERSION file.

## v0.2.0 machine-readable configuration and integrations

> 🇧🇬 Примерни политики, интеграции и инфраструктура — без автоматично прилагане на разрешения.

- [Agent registry](config/agents.yaml), [approval actions](config/approvals.yaml), [budgets](config/budgets.yaml) and the validated [Python config reader](src/bgdb_dispatch/config.py). Placeholder budgets are not enabled Paperclip limits.
- [Custom GPT instructions](intake/chatgpt/INSTRUCTIONS.md) and [OpenAPI GitHub Issue action](intake/chatgpt/openapi.yaml); create an Issue only after explicit user confirmation.
- [KSSH](integrations/kssh/README.md), [Claude Code](integrations/claude-code/README.md), [Codex](integrations/codex/README.md) and [Tailscale ACL example](infra/tailscale/acl.hujson).
- [PostgreSQL Compose](infra/postgres/docker-compose.yml), [database backup](infra/postgres/backup.sh), [Proxmox LXC dry run](infra/proxmox/create-lxc.sh) and [backup plan](infra/proxmox/backup.md).
- [Monitoring](monitoring/README.md), [agent report](scripts/agent-report.sh), [Roadmap](ROADMAP.md), [Support](SUPPORT.md) and [Bulgarian operations](docs/bg/OPERATIONS.md), [inventory](docs/bg/INVENTORY.md), [security](docs/bg/SECURITY-STANDARDS.md).
- GitHub label synchronization and tagged release workflows are added but require GitHub Actions permissions and real runs to validate.

**Note:** The existing `pyproject.toml` package metadata may still display its earlier version; `VERSION` is the release version for v0.2.0 and the package metadata should be synchronized in a later explicitly approved update.

## v0.3.0 onboarding utilities

> 🇧🇬 Новите инструменти не извършват промени без изрично разрешение.

[English Quickstart](docs/QUICKSTART.md) · [Bulgarian Quickstart](docs/bg/QUICKSTART.md) · [Agent task form](.github/ISSUE_TEMPLATE/agent-task.yml) · [Architecture decisions](docs/adr/0001-paperclip-as-dispatcher.md).

`bash scripts/doctor.sh` checks prerequisites, port 3100 and environment variables without revealing secret values. `python3 scripts/register-agents.py` prints a no-network plan; `--apply` explicitly creates missing Paperclip agent records with provisional USD budgets. Real adapter credentials, token ceilings and approval gates must be configured and verified separately.
