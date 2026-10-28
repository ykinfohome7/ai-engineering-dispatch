# KSSH integration — DevOps agent

> 🇧🇬 KSSH осигурява управляван частен SSH достъп през Tailscale.

## Available commands

> 🇧🇬 Първо диагностика, след това само одобрени операции.

The DevOps agent works through the connected KSSH app. Start with `server_test` and `tailscale_status` to check real reachability. `run_command` can be used for approved, carefully scoped read-only diagnostics; inspect every proposed shell command for side effects. For file operations use `sftp_list` / `sftp_read` for inspection and `sftp_write` / `sftp_upload` only after approval. Use the actual connected tool names, not guessed commands.

## Authentication and credentials

> 🇧🇬 Токенът остава в защитената среда, никога в Git.

Use `SSH_CONNECTOR_TOKEN` via a restricted runtime secret store, never in repository files, Issue bodies, shell history or logs. Use SSH Ed25519 authentication, Tailscale ACLs, minimal privileges and explicit target server aliases. After a Codespace restart re-check availability; for persistent connectivity move KSSH/Tailscale to an always-on Proxmox host.

## Human approval for writes

> 🇧🇬 Записите, изтриването и промяната на услуги изискват човек да одобри.

Request explicit human approval before state-changing `run_command`, `sftp_write`, `sftp_upload`, `sftp_manage`, service restarts, deployments, credential rotation, DNS changes or deletion. Present exact target, scope and rollback steps. See [approval policy](../../config/approvals.yaml), which is documentation, **not** an enforcement engine.

## Audit procedure

> 🇧🇬 Отразявай Issue, агент, действие, резултат и одобрение.

Verify target connectivity, associate a GitHub Issue, obtain the required approval, run only the authorized action and verify its result. Store redacted audit evidence in the approved monitoring system, not in public Issues.
