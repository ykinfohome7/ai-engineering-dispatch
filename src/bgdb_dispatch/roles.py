"""Deterministic role suggestions; not an AI model and not an authorization gate."""

ROLES = {
    "architect": {"name": "Architect", "keywords": ("architecture", "design", "system", "structure", "архитект", "проектира", "дизайн")},
    "developer": {"name": "Developer", "keywords": ("implement", "code", "feature", "bug", "python", "api", "разработ", "код", "функци", "поправ")},
    "reviewer": {"name": "Reviewer", "keywords": ("review", "audit", "security", "risk", "diff", "одит", "преглед", "сигурност", "провери")},
    "qa": {"name": "QA", "keywords": ("test", "quality", "regression", "coverage", "pytest", "тест", "качество")},
    "devops": {"name": "DevOps", "keywords": ("deploy", "docker", "server", "ssh", "kssh", "tailscale", "proxmox", "linux", "ci/cd", "инстали", "сървър", "връзка", "мрежа")},
    "docs": {"name": "Docs", "keywords": ("documentation", "readme", "manual", "guide", "docs", "документ", "инструкц", "ръководство")},
}


def choose_role(text: str) -> str:
    """Select most matched role; ties follow registry order, else architect."""
    text = text.casefold()
    ranked = [(sum(word in text for word in v["keywords"]), key) for key, v in ROLES.items()]
    score, role = max(ranked, key=lambda pair: pair[0])
    return role if score else "architect"
