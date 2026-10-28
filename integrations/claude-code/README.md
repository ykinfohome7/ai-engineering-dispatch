# Claude Code — engineering workflow

> 🇧🇬 Claude Code работи по Issue и публикува промени чрез PR.

## Assignment

> 🇧🇬 Търси задачите с етикет agent:developer.

Register the Claude Code adapter in Paperclip and set an individual token/USD limit before enabling it. Select an assigned open GitHub Issue with `agent:developer`; read What / Why / Done when and link the Paperclip task manually until automated synchronization has been implemented.

## Branch and pull request

> 🇧🇬 Няма директен push в main и няма самостоятелно одобрение.

Create `feat/<issue>-short-name` or `fix/<issue>-short-name` from an approved base. Implement the smallest reviewable change, run tests, update docs, and open a Pull Request referencing `Closes #<issue>`. Request review by a different agent and wait for required CI and human approval before merge.

## Safety

> 🇧🇬 Тайните, опасните команди и промените по сървъри изискват защита.

Never paste credentials into PRs or use KSSH for writes without explicit human approval. Report budget usage to Paperclip. This README does not grant additional permissions.
