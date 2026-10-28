# Architecture / Архитектура

```text
Human / ChatGPT / GitHub (task intake)
   |
   +--> BGDB AI-EMDS CLI (`plan`, `submit`, `doctor`, `list`, `get`)
                     |
                     +--> Paperclip API (issues, approvals, assignments)
                                    |
                                    +--> Architect (planning)
                                    +--> Developer (Claude Code or Codex)
                                    +--> Reviewer (human gate)
                                    +--> QA (tests)
                                    +--> DevOps (deployment; gated)
                                    +--> Docs (documentation)

GitHub: source of truth for code, PRs and version history
Codespaces: disposable development workspace, NOT production uptime
Proxmox: persistent Paperclip/KSSH/Tailscale in stage two
```

## Existing vs future integration

- Implemented: deterministic role hinting; Paperclip API issue create/read/list; optional agent-ID assignment; human opt-in before creating issues.
- Provided: Codespace definition, safe start script, nonsecret configuration template, tests.
- Not implemented: ChatGPT external Paperclip MCP integration, automatic Claude/Codex agent installation, code execution, GitHub PR automation, 24/7 KSSH gateway, live billing, approval automation.
- Paperclip controls agent orchestration, checkout, review, approval, budgets and governance; don't bypass those by directly executing shell commands from user task text.
- Recommended policy: Architect -> Developer -> Reviewer -> QA -> human approval -> DevOps -> Docs; configure actual approval rules in the Paperclip UI.

## Task flow

1. Run `plan` to view exact JSON intended for submission.
2. Configure company UUID and optional role/agent UUIDs in the shell, not Git.
3. Run `submit ... --execute` to create a `todo` issue in Paperclip.
4. Paperclip assigns/wakes installed agents only when configured and authorized.
5. Review diffs and tests before deployment. Never store credentials in issue text.
