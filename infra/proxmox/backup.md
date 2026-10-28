# Proxmox backup and recovery plan

> 🇧🇬 Архивите се конфигурират само след одобрение на реалната инфраструктура.

## Schedule and retention

> 🇧🇬 Пример: ежедневни, седмични и месечни архиви.

In the Proxmox Datacenter backup scheduler, select only the approved Paperclip and PostgreSQL LXC IDs. Example schedule: daily at 02:30 local time; retention **14 daily**, **4 weekly** and **3 monthly** backups. Use encrypted off-host storage when available. Snapshot mode requires compatible storage; use the appropriate approved mode and maintenance window.

## Manual test

> 🇧🇬 Провери контейнера и хранилището; тази команда не се изпълнява автоматично.

```bash
# Само след одобрение и подмяна на placeholder стойностите.
vzdump <APPROVED_CTID> --storage <APPROVED_BACKUP_STORAGE> --mode snapshot
```

Configure daily [PostgreSQL logical backups](../postgres/backup.sh) to a protected path outside Git. Database backups may require consistency safeguards, encryption and access policies appropriate to production.

## Restore drill

> 🇧🇬 Проверявай възстановяването в изолирана тестова среда.

Quarterly restore to new isolated test CTIDs, verify database integrity, app health and authentication, record restore duration and audit evidence. Never overwrite a live container without human approval.
