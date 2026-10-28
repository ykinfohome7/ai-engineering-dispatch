# AI-EMDS Workstreams

> 🇧🇬 Седем направления използват общите седем агента; не се създават отделни платени агенти.

## Division of responsibility

> 🇧🇬 Отделни проекти, но общ процес за проверки, бюджет и одобрения.

Workstreams are proposed Paperclip projects, not additional companies or autonomous agents. Reuse the seven existing engineering roles across domains. The proposed projects remain planned until the board enables them. Every technical change requires independent review and human approval where applicable.

| Workstream | Lead | Scope |
| --- | --- | --- |
| Networking and Cybersecurity | architect | UniFi, pfSense, Tailscale and TLS audit work, design and documentation; no live firewall or credential changes without approval. |
| Servers, DevOps and AI Infrastructure | devops | Debian, Proxmox, KSSH, Paperclip, backup restore, monitoring and CI. |
| Telephony and Communications | architect | SIP, Kamailio, FusionPBX, FreeSWITCH and UniFi Talk interoperability. |
| Business Software and ERP | developer-claude-code | ERPNext, web applications, APIs, integrations and software testing. |
| Transport and Logistics | architect | Dispatch workflow, fleet maintenance, compliance research and reports; recommendations only. |
| Energy, AI and Data Centers | architect | Technical concepts, feasibility studies, power scenarios, and AI infrastructure. |
| Research, Official Records and Documentation | docs | Verification of official records, standards, audit-ready documents and research. |

## Safeguards

> 🇧🇬 Без автоматични merge, deploy, delete, покупки, ротация на тайни или промени по сървъри.

Do not execute agents before verifying provider credentials, per-agent USD/token ceilings, company cap, and approval rules within Paperclip. The config is advisory only. Never publish private IPs, credentials or operational customer data in GitHub Issues.

## Register projects later

> 🇧🇬 Скриптът първо показва план; реалната регистрация е само с --apply.

Run python3 scripts/register-workstreams.py for a safe dry run. After the healthy **normal** Paperclip instance and a company UUID are verified, run python3 scripts/register-workstreams.py --apply using private PAPERCLIP_BASE_URL, PAPERCLIP_COMPANY_ID and optional PAPERCLIP_TOKEN environment values. This creates only missing projects with status planned; it does not start agents.

## Codespaces Rebuild warning

> 🇧🇬 Успешен рестарт на Paperclip не доказва, че база и ключове оцеляват при Rebuild.

See docs/REBUILD-VERIFY.md before replacing the Codespace container. State stored only under /home/bgadmin has not been verified to survive Rebuild.
