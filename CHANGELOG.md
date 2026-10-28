# Changelog

> 🇧🇬 История на промените по формата Keep a Changelog.

All notable changes are documented here in [Keep a Changelog](https://keepachangelog.com/en/1.1.0/) format. Versioning follows [Semantic Versioning](https://semver.org/); the canonical current version is [VERSION](VERSION).

## [Unreleased]

> 🇧🇬 Допълнителни правила, шаблони и българска документация.

### Added

> 🇧🇬 Нови документи и автоматизация, без изтриване на съществуващия код.

- Community governance files, PR and bug templates, CODEOWNERS, EditorConfig and Dependabot.
- Weekly Paperclip submodule update pull-request workflow.
- Complete Bulgarian guides for the project, architecture and agents.
- Third-party license notice and VERSION file.

## [0.3.0] - 2026-10-28

> 🇧🇬 Бърз старт, Doctor, регистратор на агенти, ADR и нови тестове.

### Added

> 🇧🇬 Подробни инструкции и безопасни средства за първоначално настройване.

- English and Bulgarian Quickstart documents, environment doctor and agent registration with dry-run by default.
- Registration unit tests, GitHub Agent task Issue form, three Architecture Decision Records.
- Bulgarian Roadmap and Contributing guides.

### Changed

> 🇧🇬 CI вече включва pytest, ShellCheck и проверка на YAML.

- Extended CI checks: pytest, ShellCheck for shell scripts, and YAML lint for config and GitHub.
- Canonical version updated to 0.3.0, inventories refreshed.

## [0.2.0] - 2026-10-28

> 🇧🇬 Добавени са конфигурации за седем агента, интеграции и примерна инфраструктура.

### Added

> 🇧🇬 Създадени са четими от програми настройки, тестове и документация.

- JSON-compatible YAML registry for seven agents, approval classes and example token/USD budgets; Python configuration validator and unit tests.
- Custom GPT intake instructions and OpenAPI 3.1 GitHub Issue action.
- KSSH, Claude Code and Codex integration instructions, private Tailscale ACL example.
- PostgreSQL 16 Compose, 14-day backup script, Proxmox Debian 12 LXC dry-run and restore policy.
- Monitoring guide, agent report, label-sync workflow and tagged ZIP release workflow.
- Support and roadmap guides, Bulgarian inventory, security and operations docs.

## [0.1.0] - 2026-10-28

> 🇧🇬 Първа версия на структурата, агентите и Paperclip интеграцията.

### Added

> 🇧🇬 Начално хранилище с инженерния диспечер и инфраструктурна документация.

- Initial BGDB AI-EMDS structure, agent roles, architecture and security documentation.
- Python intake CLI, unit tests, GitHub Actions CI and Codespaces configuration.
- Pinned Paperclip upstream Git submodule and Codespaces installation script.

[Unreleased]: https://github.com/ykinfohome7/ai-engineering-dispatch/commits/main/
[0.1.0]: https://github.com/ykinfohome7/ai-engineering-dispatch/commits/main/

[0.2.0]: https://github.com/ykinfohome7/ai-engineering-dispatch/releases/tag/v0.2.0

[0.3.0]: https://github.com/ykinfohome7/ai-engineering-dispatch/releases/tag/v0.3.0
