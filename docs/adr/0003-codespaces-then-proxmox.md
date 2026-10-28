# ADR 0003: Codespaces first, then Proxmox

> 🇧🇬 Разработката е в Codespaces, постоянната услуга е на Proxmox.

## Context

> 🇧🇬 Codespaces се спира и не може да гарантира 24/7 услуги.

Rapid prototyping is useful, but Paperclip and KSSH require persistent storage and uptime beyond Codespaces lifetime.

## Decision

> 🇧🇬 Две фази с отделна политика за непрекъсната работа.

Phase 1 uses GitHub Codespaces with Paperclip embedded PostgreSQL. Phase 2 deploys Paperclip and a private KSSH/Tailscale gateway to an approved Proxmox VM or LXC.

## Consequences

> 🇧🇬 Нужни са резервни копия, рестарт и контрол на достъпа.

Plan system services, backups, restore drills, monitoring, identity controls, migrations, and rollback before production.
