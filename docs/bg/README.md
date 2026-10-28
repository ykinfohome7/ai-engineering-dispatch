# BGDB AI-EMDS — Система за инженерно управление и разпределение на задачи

> 🇧🇬 Пълно българско ръководство към [основния README](../../README.md).

**Версия:** [VERSION](../../VERSION) — 0.1.0. **Лиценз:** [GPL-3.0](../../LICENSE). **Автор:** BGDB.EU.

BGDB AI-EMDS приема инженерни задачи чрез ChatGPT, организира ги в GitHub Issues и възлага изпълнението им чрез Paperclip на специализирани AI агенти. Първо се развива в GitHub Codespaces, после се премества на постоянно работещ Proxmox сървър. Управлението на сървърите е през частната Tailscale мрежа и KSSH.

**Реален статус:** Python intake помощникът, тестовете, CI и документацията съществуват. Реални агенти и Paperclip акаунти още трябва да бъдат регистрирани. GitHub Issue ↔ Paperclip автоматична синхронизация и постоянна Proxmox инсталация не са завършени.

## Компоненти и агенти

> 🇧🇬 ChatGPT приема, GitHub проследява, Paperclip разпределя, AI агентите изпълняват.

| Компонент | Функция |
| --- | --- |
| ChatGPT | Приемане, уточняване и планиране на задачите |
| GitHub Issue | Официално задание с критерии за завършване |
| Paperclip | Диспечер на агенти, задачи, бюджети и одобрения |
| Architect | Архитектура и разделяне на задачи |
| Developer (Claude Code) | Основна разработка |
| Developer 2 (Codex) | Независима реализация/алтернативи |
| Reviewer | Независим преглед на кода и сигурността |
| QA | Тестове и възпроизводимост |
| DevOps | CI, сървъри, внедряване и възстановяване |
| Docs | Документация и ръководства |
| KSSH + Tailscale | Контролиран частен достъп до сървъри |

## Етапи

> 🇧🇬 Codespaces е временна разработваща среда, Proxmox — постоянна.

| Етап | Среда | База данни | Цел |
| --- | --- | --- | --- |
| 1 | GitHub Codespaces | Вграден PostgreSQL на Paperclip | Разработка, настройване, тестове |
| 2 | Proxmox VM/LXC | Постоянна база, външен PostgreSQL при нужда | 24/7 достъп, резервни копия и мониторинг |

Codespaces може да бъде спрян от платформата. Когато спре, спират и локалните Paperclip, KSSH и Tailscale услуги. Автоматичният скрипт при стартиране не може да събуди вече спрял Codespace; затова се планира Proxmox.

## Бързо стартиране

> 🇧🇬 Използвайте терминала на Codespaces; порт 3100 трябва да остане частен.

1. Създайте Codespace от основния клон `main`.
2. Проверете помощника с `bash scripts/bootstrap.sh`.
3. Прегледайте ролите: `PYTHONPATH=src python3 -m bgdb_dispatch.cli roles`.
4. Стартирайте локално Paperclip: `bash dispatcher/install.sh` или `bash scripts/start-paperclip.sh`.
5. Създайте организация и регистрирайте агентите в Paperclip, след което задайте отделни бюджети и одобрения.
6. Задайте `PAPERCLIP_BASE_URL`, `PAPERCLIP_COMPANY_ID` и при необходимост токен чрез сигурната среда (не в Git).
7. Създайте локален план: `PYTHONPATH=src python3 -m bgdb_dispatch.cli plan "Review KSSH security" --role reviewer`.
8. Проверете връзката с `PYTHONPATH=src python3 -m bgdb_dispatch.cli doctor`.
9. Изпращайте към Paperclip с `submit ... --execute` само след преглед; без `--execute` изпращането е пробно.

## Правила и сигурност

> 🇧🇬 Всяка задача е Issue; директен push в main не се допуска по политиката.

Използвайте `feat/<issue>-name` или `fix/<issue>-name` клон, Pull Request, независим Reviewer и успешно CI. Активирайте GitHub branch protection/rulesets: наличието на документ само по себе си не блокира директни промени. Изтриване, промяна на ключове, DNS, production настройки, миграции и внедряване изискват изрично човешко одобрение и възможност за връщане. Не публикувайте пароли, токени, частни SSH ключове, лични данни или бази в Git.

## Структура на репозитория

> 🇧🇬 Собствените файлове не дублират изходния код на Paperclip.

| Път | Съдържание |
| --- | --- |
| `AGENTS.md`, `agents/` | Роли, политики и инструкции |
| `src/bgdb_dispatch/` | Python помощник за приемане на задачи |
| `dispatcher/paperclip/` | Git submodule към официалния Paperclip |
| `intake/chatgpt/` | ChatGPT → GitHub Issue → Paperclip |
| `infra/` | Tailscale, PostgreSQL, Proxmox |
| `docs/` | Архитектура, операции, сигурност, инвентар |
| `docs/bg/` | Български ръководства |
| `.github/` | CI, шаблони за Issue/PR, Dependabot |
| `VERSION`, `CHANGELOG.md` | Версия и промени |

## Документация, лиценз и участие

> 🇧🇬 BGDB AI-EMDS е GPL-3.0; Paperclip запазва MIT лиценза си.

[Архитектура](ARCHITECTURE.md) · [Агенти](AGENTS.md) · [Инвентар](../INVENTORY.md) · [Операции](../OPERATIONS.md) · [Сигурност](../SECURITY-STANDARDS.md) · [Принос](../../CONTRIBUTING.md) · [Поведение](../../CODE_OF_CONDUCT.md) · [История](../../CHANGELOG.md) · [Външни лицензи](../../THIRD_PARTY_NOTICES.md).
