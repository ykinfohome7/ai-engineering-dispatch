# Agent contract and governance

> 🇧🇬 Всички агенти спазват един и същ процес с Issue, отделен branch, PR и преглед.

## Roles and ownership

> 🇧🇬 Всеки агент има собствена задача и бюджет; Reviewer не е авторът на кода.

| Agent | Responsibility | Output | Budget |
|---|---|---|---|
| Architect | Requirements, technical design, issue decomposition | Plan, architecture decision | Separate per-agent cap |
| Developer (Claude Code) | Primary implementation | Branch, commits, PR | Separate per-agent cap |
| Developer 2 (Codex) | Independent implementation/alternative | Branch, commits, PR | Separate per-agent cap |
| Reviewer | Independent code/security review; must not author reviewed diff | Findings, approve/request changes | Separate per-agent cap |
| QA | Automated and manual verification | Repro steps, test evidence | Separate per-agent cap |
| DevOps | CI, networking and deployments | Approved rollout, rollback plan | Separate per-agent cap |
| Docs | READMEs, specs, operating guides | Reviewed documentation PR | Separate per-agent cap |

## Non-negotiable rules

> 🇧🇬 Няма директен push в main, тайни в кода или разрушителни операции без човешко одобрение.

1. **Every task has a GitHub Issue** with scope and acceptance criteria; link the matching Paperclip task (manual until bridge integration is built).
2. Create `feat/<issue>-short-name` or `fix/<issue>-short-name`; open a PR. **No direct pushes to `main`**. Enforce with GitHub branch protection/rulesets, which must be enabled by a repository administrator.
3. Require review by a **different agent** and passing CI; human approval is required for merging or deployment whenever policy demands. Agents may not approve their own work.
4. Destructive operations (deletion, wiping disks, force pushes, network exposure, password/key changes, DNS record changes, production configuration, database migration) require explicit **human approval** and a rollback plan.
5. Set a **token/cost budget for each agent in Paperclip** before activation, with spend limits and manual escalation; no unlimited defaults. Budget enforcement is a Paperclip configuration step, not something these documents automatically apply.
6. **Never place secrets in code, prompts, Issues, PRs, logs, or Git history.** Use restricted GitHub secret stores or secure runtime secret injection. No account tokens may be pasted into an agent conversation.
7. Prefer read-only inspection; keep access scoped to repositories and Tailscale-protected hosts. Use KSSH only for explicitly approved operations.
8. Review upstream changes and pin dependency revisions; do not silently update the Paperclip submodule.

## Execution order

> 🇧🇬 Примерен маршрут: архитект → разработка → независим преглед → тест → документи → одобрено внедряване.

`GitHub Issue → Architect → Developer (Claude/Codex) → independent Reviewer → QA → Docs → CI → human-approved merge → DevOps (if needed)`.
