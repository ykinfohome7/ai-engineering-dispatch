"""Подсказва роля по ключови думи; това не е AI или проверка на права."""

ROLES = {
    "architect": {"name": "Architect", "keywords": ("architecture", "design", "system", "structure", "архитект", "проектира", "дизайн")},
    "developer": {"name": "Developer", "keywords": ("implement", "code", "feature", "bug", "python", "api", "разработ", "код", "функци", "поправ")},
    "developer_codex": {"name": "Developer 2 (Codex)", "keywords": ("codex", "developer 2", "openai coding", "втори разработчик")},
    "reviewer": {"name": "Reviewer", "keywords": ("review", "audit", "security", "risk", "diff", "одит", "преглед", "сигурност", "провери")},
    "qa": {"name": "QA", "keywords": ("test", "quality", "regression", "coverage", "pytest", "тест", "качество")},
    "devops": {"name": "DevOps", "keywords": ("deploy", "docker", "server", "ssh", "kssh", "tailscale", "proxmox", "linux", "ci/cd", "инстали", "сървър", "връзка", "мрежа")},
    "docs": {"name": "Docs", "keywords": ("documentation", "readme", "manual", "guide", "docs", "документ", "инструкц", "ръководство")},
}


def choose_role(text: str) -> str:
    """Избира роля по съвпадения; при равен резултат следва реда в речника."""
    text = text.casefold()
    # Явна заявка за Codex има предимство пред общите думи за разработка.
    if "codex" in text or "developer 2" in text:
        return "developer_codex"
    ranked = [(sum(word in text for word in v["keywords"]), key) for key, v in ROLES.items()]
    score, role = max(ranked, key=lambda pair: pair[0])
    return role if score else "architect"
