# BGDB AI-EMDS v0.3.0 — Бърз старт

> 🇧🇬 Български вариант на [Quickstart](../QUICKSTART.md).

## 1. Отвори Codespace

> 🇧🇬 Code → Codespaces → Create codespace on main.

Отвори [проекта в GitHub](https://github.com/ykinfohome7/ai-engineering-dispatch) и избери клона `main`. Изчакай devcontainer. Codespaces е временна среда; портовете остават **Private**.

## 2. Провери тайните

> 🇧🇬 Никакви ключове и пароли в Git, логове или публични Issues.

Използвай Codespaces Secrets или защитена среда. [.env.example](../../.env.example) съдържа само имена. За Paperclip трябват PAPERCLIP_BASE_URL, истинският UUID на PAPERCLIP_COMPANY_ID и при необходимост PAPERCLIP_TOKEN. За Claude и Codex настрой тайните в реалните им адаптери.

## 3. Проверка на средата

> 🇧🇬 Диагностиката показва единствено SET/MISSING.

```bash
bash scripts/doctor.sh
```

Проверява Node >=24.11, pnpm, python3, gh, git, Paperclip submodule, променливи на средата и дали порт 3100 е свободен. Ако submodule липсва, пусни `git submodule update --init --recursive`. Ако портът е зает, Paperclip може вече да работи. За Python тестове: `bash scripts/bootstrap.sh`.

## 4. Инсталирай Paperclip

> 🇧🇬 Отвори частния порт 3100, без публичен Funnel.

```bash
bash dispatcher/install.sh
```

Завърши началната настройка. В секцията **Ports** отвори **3100 → Open in Browser** и провери видимост **Private**. Не публикувай интерфейса в интернет.

## 5. Регистрирай седемте агента

> 🇧🇬 Dry-run не изпраща заявки; --apply създава записи.

Създай организация в Paperclip и задай действителния `PAPERCLIP_COMPANY_ID` в защитената среда. Прегледай имената и бюджетите:

```bash
python3 scripts/register-agents.py
```

След преглед и изрично съгласие:

```bash
python3 scripts/register-agents.py --apply
```

Скриптът избягва дублиране на съществуващи имена и задава примерни USD лимити. Той **не** активира автоматично истински модели, токенни лимити, разрешения, човешки одобрения и KSSH. Настрой ги отделно, преди да разрешиш работа по реални задачи.

## 6. Създай първата задача

> 🇧🇬 Всяко задание започва с GitHub Issue.

В [New Issue](https://github.com/ykinfohome7/ai-engineering-dispatch/issues/new/choose) избери **Agent task**. Попълни заглавие, описание, Done when, агент и при нужда отметката за одобрение. Добави ръчно `agent:*` етикета — dropdown изборът не го задава автоматично. Връзката с Paperclip остава ръчна, докато няма работещ мост.

## 7. Финална проверка

> 🇧🇬 Успешният CI не означава готова продукционна услуга.

Провери [GitHub Actions](https://github.com/ykinfohome7/ai-engineering-dispatch/actions), ролите, бюджетите, реалните одобрения и защитата на `main`. Прочети [инвентара](INVENTORY.md).
