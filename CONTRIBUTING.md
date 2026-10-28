# Contributing to BGDB AI-EMDS

> 🇧🇬 Приносите минават през Issue, feature branch, PR и одобрение.

## Workflow

> 🇧🇬 Не се пише директно в main; първо се описва задачата.

1. Open a GitHub Issue (use the [task template](.github/ISSUE_TEMPLATE/task.md)) and define "Done when".
2. Branch from current `main`: `git switch -c feat/<issue>-short-name` (or `fix/<issue>-short-name`).
3. Make a focused change without secrets or unrelated formatting churn.
4. Run `bash scripts/bootstrap.sh` and any task-specific checks; update or add tests.
5. Open a PR referencing `Closes #<issue>`. Obtain independent review, passing CI and any required human approval.
6. Merge using repository policy; keep protected `main` free of direct agent pushes.

## Licensing and upstream

> 🇧🇬 Нашият код е GPL-3.0; Paperclip има отделен MIT лиценз.

Contributions to this repository are offered under **GPL-3.0** as documented in [LICENSE](LICENSE). The Paperclip git submodule retains its separate **MIT** license and history. Never copy upstream source into our repository when a pinned submodule suffices.
