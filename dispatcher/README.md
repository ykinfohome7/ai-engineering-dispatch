# Paperclip dispatcher

> 🇧🇬 Paperclip разпределя задачите, контролира агентите, лимитите и одобренията.

## Source and pinned submodule

> 🇧🇬 Понеже fork-ът не е достъпен, временно използваме оригиналния upstream.

Requested fork: https://github.com/ykinfohome7/paperclip . On 2026-10-28 this repository returned **404** to the connected GitHub account. For a functional fresh clone, `dispatcher/paperclip` points to https://github.com/paperclipai/paperclip (upstream, **MIT**) and a fixed commit. After creating/granting access to the fork, update `.gitmodules` and the submodule SHA in a reviewed PR. This directory is **not** a copy of Paperclip files.

## Install and run in Codespaces

> 🇧🇬 Нужни са Node >=24.11, pnpm 9.15.4 и частен порт 3100.

```bash
bash dispatcher/install.sh
```

The launcher checks Node.js and pnpm, initializes the submodule, runs `pnpm install --frozen-lockfile`, then `pnpm dev` inside the upstream checkout. Codespaces forwards port **3100**; keep port visibility **Private**. The first launch may require upstream onboarding/configuration; check its console output. Phase 1 uses Paperclip's **embedded PostgreSQL**; an external `DATABASE_URL` is unnecessary.

## Pending setup

> 🇧🇬 Тези действия още не са изпълнени автоматично.

- Install/onboard Paperclip and create BGDB organization/company.
- Register seven logical roles with actual Claude Code/Codex adapters; configure token/cost budgets **per agent**.
- Require human approvals for destructive changes, deployments, secrets and production access.
- Connect GitHub Issues to Paperclip issues with a verified link; automate only after review.
- Back up persistent state before promoting to Proxmox; enable access controls.
