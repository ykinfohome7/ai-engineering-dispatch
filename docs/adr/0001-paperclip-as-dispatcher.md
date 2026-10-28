# ADR 0001: Paperclip as dispatcher

> 🇧🇬 Paperclip управлява заданията, агентите и разходите.

## Context

> 🇧🇬 Нуждаем се от състояние, бюджети и контрол на отделни AI агенти.

The project needs an auditable agent organization, assignment system, budgets, and human approvals.

## Decision

> 🇧🇬 Използваме Paperclip, а Python intake остава помощник.

Use pinned upstream Paperclip as the dispatcher. ChatGPT receives tasks; GitHub tracks Issues/PRs; the Python helper assists with intake.

## Consequences

> 🇧🇬 Истинските адаптери и одобрения трябва да се конфигурират в Paperclip.

Actual agents, budgets, authentication and approval gates must be onboarded. Repository YAML describes intended policy but does not enforce access.
