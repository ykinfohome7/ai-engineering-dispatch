# PostgreSQL storage

> 🇧🇬 В Codespaces не е нужен отделен PostgreSQL контейнер.

## Phase 1 — embedded database

> 🇧🇬 Paperclip използва вградена PostgreSQL среда при локален старт.

Use Paperclip's documented local embedded PostgreSQL. Do not set external `DATABASE_URL` unless the selected upstream release specifically requires it. Codespaces disk/processes are not a production database or high-availability backup system.

## Phase 2 — durable database

> 🇧🇬 За Proxmox използвай постоянен диск, архиви и отделен DB потребител.

Plan an external PostgreSQL service with restricted Tailnet-only connectivity, application-specific credentials supplied through secrets, encrypted backups plus tested restore, versioned migrations, patch management, and resource monitoring. Confirm upstream version compatibility before deployment. Never expose PostgreSQL port 5432 publicly.
