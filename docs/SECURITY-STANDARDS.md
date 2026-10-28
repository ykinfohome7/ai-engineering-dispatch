# Security standards and key lifecycle

> 🇧🇬 Задължителни правила за SSH, тайни, мрежова изолация и одобрения.

## SSH cryptography

> 🇧🇬 Използвай Ed25519 по подразбиране; RSA 4096 само при реална необходимост.

Default to **Ed25519** SSH keys. For systems that cannot support Ed25519, use **RSA 4096** with SHA-2 signatures, never SHA-1 `ssh-rsa` signatures. Enforce host key checking, per-operator keys, restricted privileges and MFA at the identity layer where available. Before disabling root login/password authentication, verify an unprivileged user can connect using a key. Then set `PermitRootLogin no` and `PasswordAuthentication no` and validate configuration before reload.

## Rotation and secrets

> 🇧🇬 Планирай подмяна на ключовете между 40 и 90 дни; при компрометиране — незабавно.

Adopt a **40–90 day internal rotation target** for SSH/API credentials based on risk; this is a BGDB operational policy, not a universal standards mandate. Revoke and replace immediately after exposure or personnel change. Keep private keys, token values, database passwords and full cert key material out of Git, Issues, PRs, chat prompts, tests and logs. Use scoped secret storage; CI pattern checks provide only defense in depth, not a complete detector.

## Private connectivity and release controls

> 🇧🇬 Сървърите са достъпни само през Tailscale и одобрени KSSH операции.

Restrict infrastructure administration to Tailnet ACLs and host firewalls; do not expose SSH, PostgreSQL, KSSH/MCP or privileged Paperclip dashboards to the public internet. Keep Codespaces port 3100 Private. Require human approval before destructive operations, production deployments, DNS changes, key rotation, infrastructure/network edits or forced Git updates. Record the approval and planned rollback path in the Issue.
