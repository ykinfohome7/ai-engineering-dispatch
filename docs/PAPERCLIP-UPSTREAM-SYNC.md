# Paperclip upstream pin review — 2026-11-05

This change updates the pinned Git submodule `dispatcher/paperclip` in BGDB AI-EMDS.

- Upstream: https://github.com/paperclipai/paperclip
- Previous pinned SHA: `f8226b0515634f9c7c74e80bb6cf18f3c2634c12`
- Proposed pinned SHA: `c656b95b6b00e029b4661e93499eade37508f425`
- Upstream comparison: 559 commits ahead, 0 behind (as checked on 2026-11-05).
- BGDB AI-EMDS wrapper stays at `0.3.0`; this is an upstream submodule update, not a wrapper release.

## Review and validation

1. Inspect upstream changes and release/migration notes between the pinned SHAs.
2. Check the supported Node/pnpm versions and database migration implications before running Paperclip.
3. In an isolated, private Codespace or throwaway test environment, run:
   ```bash
   git submodule update --init --recursive
   bash scripts/doctor.sh
   bash scripts/bootstrap.sh
   ```
4. Only after checking compatibility, run `bash scripts/start-paperclip.sh` in that isolated environment. Keep port 3100 private.
5. Do not merge to `main` or deploy to Proxmox/KSSH until the integration has passed review.

## Revert

A rollback of this change only requires restoring the previous gitlink SHA in
`dispatcher/paperclip` to `f8226b0515634f9c7c74e80bb6cf18f3c2634c12`,
and running `git submodule update --init --recursive` in the checkout.
This does **not** roll back any database migrations or external state changes made
by starting the newer application. Back up databases before any future deployment.
