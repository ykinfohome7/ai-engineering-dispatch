# BGDB AI-EMDS — AI Engineering Management & Dispatch System

Initial **v0.1.0 (MVP)** for `ykinfohome7/ai-engineering-dispatch`. ChatGPT/user supplies an engineering task, this lightweight CLI prepares and optionally creates a **Paperclip** issue, and Paperclip manages real AI agent assignment, budgets and approvals. Works first in a private GitHub Codespace; production target is an always-on Proxmox VM using Tailscale and KSSH.

> **Current status:** CLI and tests are implemented. Paperclip, agent adapters (Claude Code/Codex), Tailscale/KSSH and a persistent deployment **are not yet installed or connected by this repository**. No shell commands from task descriptions are executed.

## Quickstart (Codespaces)

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

| Role | Responsibility | Agent option |
| --- | --- | --- |
| Architect | design, decomposition | Claude Code / Codex |
| Developer | implementation | Claude Code / Codex |
| Reviewer | architecture/security review | Claude Code / Codex + human |
| QA | automated tests, reproducibility | Claude Code / Codex |
| DevOps | build, environment, deploy | Claude Code / Codex; approval gate |
| Docs | documentation and runbooks | Claude Code / Codex |

## Security & uptime

Repository is **public**. Never commit any credentials. The CLI allows HTTP only on localhost and requires HTTPS + token for remote URLs. Keep Codespaces forwarded ports private. A Codespace automatically stops and cannot keep KSSH/Paperclip running 24/7; move the gateway and service to a Proxmox VM for persistent availability. See [Operations](docs/OPERATIONS.md) and [Architecture](docs/ARCHITECTURE.md).

**Upstream:** [Paperclip](https://github.com/paperclipai/paperclip) — use its documented [Issues API](https://github.com/paperclipai/paperclip/blob/master/docs/api/issues.md).

**License:** GPL-3.0 (existing repository license). Contributions welcome.
