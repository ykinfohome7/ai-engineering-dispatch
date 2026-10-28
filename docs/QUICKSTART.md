# Quickstart — BGDB AI-EMDS v0.3.0

> 🇧🇬 Стъпки за безопасно стартиране от нулата в GitHub Codespaces.

## 1. Open a Codespace

> 🇧🇬 GitHub → Code → Codespaces → Create codespace on main.

Visit [the project](https://github.com/ykinfohome7/ai-engineering-dispatch) and create a Codespace on **main**. Complete devcontainer setup. Codespaces is a temporary development environment, not a 24/7 host. Keep forwarded ports **Private**.

## 2. Check secrets privately

> 🇧🇬 Не поставяй пароли и токени в GitHub код или Issues.

Configure GitHub Codespaces Secrets or a secure runtime credential store. See [.env.example](../.env.example) for variable names only. Local Paperclip uses PAPERCLIP_BASE_URL (normally 127.0.0.1:3100), PAPERCLIP_COMPANY_ID after onboarding, and PAPERCLIP_TOKEN if required. Claude/Codex credentials must be configured privately in their Paperclip adapters. Do not insert live secrets in any repository files.

## 3. Run the doctor

> 🇧🇬 Провери софтуера, submodule и порт 3100 без разкриване на секрети.

```bash
bash scripts/doctor.sh
```

Doctor checks Node.js >= 24.11, pnpm, python3, gh, git, Paperclip submodule, SET/MISSING environment variable status, and whether loopback port 3100 is free. Missing optional secrets do not count as failed prerequisites. If the submodule is missing, run `git submodule update --init --recursive`. If Paperclip is already running, the port will be occupied. Run `bash scripts/bootstrap.sh` to execute existing tests.

## 4. Install and open Paperclip

> 🇧🇬 Стартирай Paperclip само на частния Codespaces порт.

```bash
bash dispatcher/install.sh
```

Follow Paperclip onboarding. In the Codespaces **Ports** panel select port **3100 → Open in Browser** and confirm its visibility is **Private**. Never make it public or use a Tailscale Funnel as a shortcut.

## 5. Register seven agents

> 🇧🇬 Без --apply няма API заявки и промени.

In the Paperclip UI create the BGDB company, obtain its actual UUID and set PAPERCLIP_COMPANY_ID in a private environment. Preview the configured agents:

```bash
python3 scripts/register-agents.py
```

After inspecting names and placeholder USD budgets, explicitly create missing agent records:

```bash
python3 scripts/register-agents.py --apply
```

The script checks existing names/budgets to avoid duplicates, but does **not** configure model credentials, token ceilings, real approval enforcement or KSSH connectivity. Configure and verify adapters, budgets and approvals in Paperclip before assigning work. KSSH is an independent integration, not a native Paperclip adapter.

## 6. Create the first GitHub Issue

> 🇧🇬 Попълни критериите за завършване и избери подходящ агент.

Open [New Issue → Agent task](https://github.com/ykinfohome7/ai-engineering-dispatch/issues/new/choose). Fill in the title, description, Done when, agent dropdown and the Needs human approval checkbox for sensitive changes. Select the corresponding `agent:*` label manually; GitHub dropdown selections do **not** automatically add labels. If using a custom GPT, confirm before creating the Issue. The GitHub Issue ↔ Paperclip bridge is not yet implemented; link tasks manually.

## 7. Check readiness

> 🇧🇬 Зелен CI не означава готова продукционна инсталация.

Review [Actions](https://github.com/ykinfohome7/ai-engineering-dispatch/actions), actual agent setup, approval gates, branch protection and independent reviews. Follow [Inventory](INVENTORY.md) and [Bulgarian quickstart](bg/QUICKSTART.md) for remaining steps.
