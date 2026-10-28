# ChatGPT task intake

> 🇧🇬 ChatGPT описва задачата, но не стартира сам код или опасни действия.

## Contract

> 🇧🇬 Всяка задача получава GitHub Issue и връзка към съответната задача в Paperclip.

`User → ChatGPT (scope, acceptance criteria, agent hint) → GitHub Issue → Paperclip issue → assigned agent → PR → CI + review → merge`.

Use the issue template with **What / Why / Done when / Agent**, link relevant repository/file context and risk/approval requirements; omit secrets. A human or authorized GitHub integration creates the Issue. The current Python CLI can prepare and submit a **Paperclip issue** after the GitHub Issue exists but does **not** currently create/link GitHub Issues automatically. Keep both issue URLs cross-referenced manually until synchronization is implemented and tested.

## Optional local CLI

> 🇧🇬 `plan` не променя нищо; `submit --execute` изпраща към Paperclip само след разрешение.

```bash
PYTHONPATH=src python3 -m bgdb_dispatch.cli roles
PYTHONPATH=src python3 -m bgdb_dispatch.cli plan 'Add reconnect test' --role qa
# Configure PAPERCLIP_COMPANY_ID and credentials privately before submitting.
PYTHONPATH=src python3 -m bgdb_dispatch.cli submit 'Add reconnect test' --role qa --execute
```
