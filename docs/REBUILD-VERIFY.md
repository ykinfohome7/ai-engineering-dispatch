# Codespace Rebuild Verification

> 🇧🇬 Следи рестарт и Rebuild поотделно; не изтривай временната среда без архив.

## Three different checks

> 🇧🇬 Рестарт на Paperclip, Stop/Start и Rebuild не са еквивалентни.

1. **Paperclip restart**: stop only Paperclip and restart from the BGDB boot script. Verify SSH port 2222 remains available and the private Paperclip /api/health returns HTTP 200 on 127.0.0.1:3100.
2. **Codespace Stop/Start**: use GitHub Codespaces to stop and wake the Codespace. Check KSSH/SSH, Tailscale state, Paperclip health and database/company counts after the boot script runs.
3. **Codespace Rebuild Container**: replace only after verified persistent storage and recoverable backups. A healthy empty Paperclip instance does not mean the old state survived.

## Important persistence risk

> 🇧🇬 Папките под /home/bgadmin не са потвърдени като постоянни volumes при Rebuild.

The first deployment used /home/bgadmin/ai-engineering-dispatch and /home/bgadmin/.paperclip-worktrees/instances/bgdb-ai-emds for source and database. BGDB's checked-in devcontainer does not explicitly declare a persistent named volume for this home directory. Do not rebuild against unbacked data. Also preserve Tailscale identity and connector credentials using supported secret storage, never public Git.

## Read-only health check

> 🇧🇬 Скриптът не изписва ключове и токени и не прави промени.

Run bash scripts/check-codespace-rebuild.sh before and after each transition; it reports SSH, Paperclip, database and persistence risk. This diagnostic is not a backup or proof that the data will survive.

## Acceptance checklist

> 🇧🇬 Пълен PASS има само при работеща връзка и съхранени данни.

- [ ] SSH/KSSH reconnect and Tailscale identity verified.
- [ ] Paperclip health returns HTTP 200 on localhost port 3100.
- [ ] Same company UUID and agent roster verified before and after Stop/Start.
- [ ] Database and secret files on proven persistent storage.
- [ ] Encrypted backup restored in a separate test instance.
- [ ] Same company UUID and roster verified after an actual Rebuild.
- [ ] No public Codespaces ports or exposed tokens.
