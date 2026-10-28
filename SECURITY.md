# Security policy

> 🇧🇬 Съобщавай уязвимости поверително, а не чрез публичен Issue.

## Private vulnerability reporting

> 🇧🇬 Използвай GitHub Security Advisories и настройките за поверително съобщаване.

Open the repository [Security tab](https://github.com/ykinfohome7/ai-engineering-dispatch/security) and use **Report a vulnerability** if private vulnerability reporting is enabled. If the button is unavailable, contact the repository administrators privately and request a secure reporting channel; do **not** put proof-of-concept secrets in a public issue or discussion. Never include live access tokens, private keys or real user data in reports.

## Supported deployment posture

> 🇧🇬 Публичният репозиториум не означава публичен достъп до сървърите.

The project is in early development. The Python CLI permits cleartext HTTP only on loopback; for remote Paperclip endpoints use HTTPS and a scoped token. Codespaces port 3100 must remain private. Paperclip/KSSH on Proxmox should only be reachable via Tailnet ACLs and required authentication. See [Security standards](docs/SECURITY-STANDARDS.md).

## Response process

> 🇧🇬 Първо потвърждение и ограничаване, после поправка и проверка.

Maintainers should triage privately, validate impact, revoke exposed credentials as needed, patch on a restricted branch, and disclose only after remediation. Report upstream Paperclip vulnerabilities to its maintainers separately.
