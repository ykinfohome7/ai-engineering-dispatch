# Operations, restart recovery and security

> 🇧🇬 Прегледай реалните версии и статуса преди стартиране или промени.

## GitHub Codespaces (development)

> 🇧🇬 Инсталирай локалния Paperclip submodule с един общ скрипт.

1. Create Codespace from this repo (`main`). `.devcontainer` installs Python and Node 24.
2. `bash scripts/bootstrap.sh` for local tests; run `PYTHONPATH=src python3 -m bgdb_dispatch.cli roles`.
3. `bash scripts/start-paperclip.sh` starts Paperclip on local loopback. This wrapper delegates to `dispatcher/install.sh` for the pinned Paperclip submodule. The first onboarding may require interaction. Confirm the printed dashboard URL.
4. Create a Paperclip company and agent accounts, then set `PAPERCLIP_COMPANY_ID` in your shell.
5. Test `PYTHONPATH=src python3 -m bgdb_dispatch.cli plan "Implement status page" --role developer`.
6. Test connection with `doctor` after the company is created; use `submit ... --execute` only when ready.

## The KSSH / Codespace lifecycle problem

> 🇧🇬 Codespace и неговите услуги не работят, когато средата е спряна.

GitHub Codespaces stops processes when a codespace stops; local Tailscale, SSH, MCP/KSSH and Paperclip servers die with it. `postStartCommand` only runs **after a person/platform starts the Codespace again**. It cannot wake a stopped Codespace from inside itself. GitHub also enforces a maximum runtime; no bootstrap script can guarantee 24/7 Codespace uptime.

The repo intentionally does not auto-open a public Tailscale Funnel, inject SSH passwords, or bind Paperclip to 0.0.0.0. Before any internet exposure, use authenticated mode, TLS, origin/hostname restrictions, and least-privilege tokens.

**Reliable arrangement:** deploy the Paperclip server + KSSH gateway + Tailscale connector to an always-on Proxmox VM (e.g. Debian 13), with persistent storage and systemd units. Keep GitHub Codespaces for temporary development; connect to the persistent service. Configure Tailscale ACLs and host-level firewall to only admit authorized users. Do not expose private MCP endpoints publicly without authentication.

## Security checklist

> 🇧🇬 Не излагай Dashboard или KSSH публично и не пази тайни в Git.

- Repo is **public**: no Tailscale auth keys, MCP bearer tokens, SSH private keys, API keys, passwords, `.env`, database snapshots or certificate private keys.
- GitHub Codespaces port 3100 stays **private**; never change port visibility to Public for authenticated dashboard/data.
- Use Ed25519 SSH keys, disable root SSH login and password authentication after checking working key access.
- Keep TLS validation enabled; client refuses remote cleartext HTTP.
- Use review gates for destructive operations, PR merging, credentials, deployments and infrastructure changes.
- Disable idle/expensive agents until budgets and limits are configured in Paperclip.
- Make periodic encrypted backups of the Paperclip database, configuration and agent state on Proxmox.
