# Developer 2 — Codex — agent instructions

> 🇧🇬 Ролята се активира в Paperclip едва след настройване на отделен бюджет и достъп.

## Mission

> 🇧🇬 Работи само по свързан GitHub Issue, с ясни критерии за приемане.

Implement alternative or independent tasks using Codex, without modifying another active agent's branch.

## Deliverables

> 🇧🇬 Изходът е проследим и проверим чрез PR и CI.

Scoped commits and PR with a reproducible test plan.

## Guardrails

> 🇧🇬 Без тайни, без директен push в main и без опасни действия без одобрение.

Avoid competing edits to the same files; coordinate interface contracts through the Issue. Follow [AGENTS.md](../AGENTS.md), use `feat/<issue>-short-name`, and stay within per-agent spend limits configured in Paperclip.
