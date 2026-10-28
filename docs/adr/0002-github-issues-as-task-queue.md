# ADR 0002: GitHub Issues as task queue

> 🇧🇬 Всеки инженерeн проект започва с GitHub Issue.

## Context

> 🇧🇬 Изискванията и резултатите трябва да бъдат проследими.

Changes need documented ownership, acceptance criteria, independent review, and links to commits and pull requests.

## Decision

> 🇧🇬 Issue → отделен branch → PR → CI → независим review.

Every engineering task is a GitHub Issue. Agents work in named branches and propose a pull request; no direct push to main.

## Consequences

> 🇧🇬 Връзката с Paperclip е ръчна, докато не се реализира надежден мост.

GitHub-to-Paperclip synchronization must be authenticated and idempotent to prevent duplicate work. Branch protection must be enabled separately.
