# Monitoring and audit trail

> 🇧🇬 Следим агентите, задачите, разходите и човешките одобрения.

## Required fields

> 🇧🇬 Записвай само необходимите данни, без тайни и лична информация.

Track timestamp (UTC), agent identifier, GitHub Issue/PR, action name, status, token/USD cost if available, required approval and approving human. Do not log SSH private keys, access tokens, passwords, database records or private customer data. Redact diagnostics and restrict log access.

## Sources of record

> 🇧🇬 Paperclip и GitHub съхраняват различни части от историята.

Paperclip: registered agents, assignments, budgets and approval decisions after configuration. GitHub: Issues, PRs, reviews, CI and releases. Use the [agent report script](../scripts/agent-report.sh) to inspect open work. The YAML configuration alone does not enforce approvals or generate telemetry.

## Weekly review

> 🇧🇬 Всяка седмица преглеждай разходи, грешки и висящи одобрения.

Compare Paperclip tasks against GitHub Issues, identify failed CI and unreviewed PRs, inspect actual spend and agent budget alerts, check KSSH/Tailscale availability, backup age and restore test history. Define alert routing and retention after production deployment; this documentation does not enable alerts automatically.
