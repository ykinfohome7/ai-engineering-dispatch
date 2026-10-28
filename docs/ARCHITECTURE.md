# System architecture

> 🇧🇬 ChatGPT приема задачата, GitHub я проследява, Paperclip управлява агентите и ресурсите.

## Target control and execution plane

> 🇧🇬 Схемата показва целевия поток; автоматичният мост GitHub → Paperclip още е TODO.

```text
    User
     |
     v
 ChatGPT (intake: What / Why / Done when)
     |
     v
 GitHub Issue  -- [manual link for now] -->  Paperclip dispatcher
     |                                     /    |       \
     |                              embedded PG      budgets/approvals
     |                              (phase 1)          |
     |                                          +------+------+-------+
     |                                          |      |      |       |
     |                                      Architect Dev 1  Dev 2  Reviewer
     |                                          |  (Claude) (Codex)  QA/Docs
     +------------------------------------------+------+------+-------+
                                                |
                                          feat/<issue>-name
                                                |
                                             GitHub PR
                                                |
                                       independent review + CI
                                                |
                                          approved merge
                                                |
                                              DevOps
                                                |
                                         KSSH (MCP gateway)
                                                |
                                          Tailscale / ACL
                                                |
                                      authorized servers / Proxmox
```

## Components and ownership

> 🇧🇬 Използвай един инсталационен път, без дублиране на Paperclip или функциите му.

- **Intake:** GitHub Issues + optional `src/bgdb_dispatch` Paperclip REST helper. Python helper is **not** a GitHub bridge or agent runner.
- **Paperclip:** org, issues, agent assignments, approvals, budgets and local embedded PostgreSQL. Source is a pinned upstream submodule.
- **Agents:** Architect, Developer (Claude Code), Developer 2 (Codex), Reviewer, QA, DevOps, Docs. Configuring real adapters is a manual step.
- **GitHub:** source control, PRs, branch policy and CI. Enforce protection in GitHub settings.
- **KSSH/Tailscale:** approved, authenticated private server access. A stopped Codespace cannot be an always-on gateway.
- **Proxmox:** phase-2 persistent runtime and database; no deployment performed by this scaffold.

## Gaps and sequencing

> 🇧🇬 Задачите за свързване, агентите и продукционната миграция остават за отделни Issues.

1. Configure real Paperclip agents and individual spending budgets.
2. Implement an authenticated, idempotent GitHub Issue ↔ Paperclip issue sync; avoid duplicate tasks and loops.
3. Protect `main` with mandatory PR review, status checks and human release approvals.
4. Deploy persistent Paperclip/KSSH/Tailscale on Proxmox with backup and restore tests.
