"""Проверка на примерните YAML настройки без външни зависимости.

Файловете са JSON-подмножество на YAML 1.2; тази проверка НЕ прилага права.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

AGENT_IDS = frozenset(
    {
        "architect",
        "developer-claude-code",
        "developer-codex",
        "reviewer",
        "qa-tester",
        "devops",
        "docs",
    }
)
APPROVAL_ACTIONS = frozenset(
    {"merge_to_main", "deploy", "delete", "server_changes", "secret_rotation"}
)
DEFAULT_CONFIG_DIR = Path(__file__).resolve().parents[2] / "config"


class ConfigError(ValueError):
    """Грешка при четене или проверка на примерните настройки."""


def _read_yaml_subset(path: Path) -> dict[str, Any]:
    """Чете YAML 1.2, записан в строгия JSON-съвместим формат."""
    try:
        content = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        raise ConfigError(f"Cannot load {path.name}: {exc}") from exc
    if not isinstance(content, dict):
        raise ConfigError(f"{path.name}: expected a mapping")
    return content


def _positive_number(value: Any, name: str) -> None:
    """Отхвърля нули, булеви стойности и невалидни лимити."""
    if isinstance(value, bool) or not isinstance(value, (int, float)) or not (0 < value < float("inf")):
        raise ConfigError(f"{name}: expected a finite positive number")


def _positive_integer(value: Any, name: str) -> None:
    """Проверява лимита за токени като положително цяло число."""
    if isinstance(value, bool) or not isinstance(value, int) or value <= 0:
        raise ConfigError(f"{name}: expected a positive integer")


def load_config(config_dir: str | Path | None = None) -> dict[str, dict[str, Any]]:
    """Зарежда трите файла и проверява съответствието между тях."""
    directory = Path(config_dir) if config_dir is not None else DEFAULT_CONFIG_DIR
    agents = _read_yaml_subset(directory / "agents.yaml")
    approvals = _read_yaml_subset(directory / "approvals.yaml")
    budgets = _read_yaml_subset(directory / "budgets.yaml")

    for name, data in (("agents", agents), ("approvals", approvals), ("budgets", budgets)):
        if data.get("version") != 1 or data.get("placeholder_only") is not True:
            raise ConfigError(f"{name}: expected version=1 and placeholder_only=true")

    entries = agents.get("agents")
    if not isinstance(entries, list) or len(entries) != len(AGENT_IDS):
        raise ConfigError("agents: exactly seven entries required")
    by_id = {}
    for entry in entries:
        if not isinstance(entry, dict) or not isinstance(entry.get("id"), str):
            raise ConfigError("agents: entry must include id")
        name = entry["id"]
        if name in by_id or name not in AGENT_IDS:
            raise ConfigError(f"agents: duplicate or unknown id {name}")
        for field in ("role", "tool"):
            if not isinstance(entry.get(field), str) or not entry[field].strip():
                raise ConfigError(f"{name}: missing {field}")
        allowed = entry.get("allowed_actions")
        required = entry.get("needs_approval")
        if not isinstance(allowed, list) or not allowed or not all(isinstance(a, str) and a for a in allowed):
            raise ConfigError(f"{name}: invalid allowed_actions")
        if len(allowed) != len(set(allowed)):
            raise ConfigError(f"{name}: duplicate allowed_actions")
        if not isinstance(required, list) or not all(isinstance(a, str) for a in required):
            raise ConfigError(f"{name}: invalid needs_approval")
        if len(required) != len(set(required)) or not set(required) <= APPROVAL_ACTIONS:
            raise ConfigError(f"{name}: unknown/duplicate approval actions")
        _positive_number(entry.get("monthly_budget_usd"), f"{name}.monthly_budget_usd")
        by_id[name] = entry

    if set(by_id) != AGENT_IDS:
        raise ConfigError("agents: missing required role")
    approval_entries = approvals.get("actions")
    if not isinstance(approval_entries, list):
        raise ConfigError("approvals: actions must be an array")
    approval_ids = []
    for action in approval_entries:
        if not isinstance(action, dict) or action.get("actor") != "human" or action.get("audit_required") is not True:
            raise ConfigError("approvals: every action needs a human and audit")
        _positive_integer(action.get("required_approvers"), "required_approvers")
        approval_ids.append(action.get("id"))
    if len(approval_ids) != len(APPROVAL_ACTIONS) or set(approval_ids) != APPROVAL_ACTIONS:
        raise ConfigError("approvals: missing, duplicate or unknown action")
    if approvals.get("default_decision") != "deny_until_human_approval":
        raise ConfigError("approvals: unsafe default decision")
    if budgets.get("currency") != "USD":
        raise ConfigError("budgets: currency must be USD")
    _positive_number(budgets.get("global_monthly_limit_usd"), "global_monthly_limit_usd")
    limits = budgets.get("agents")
    if not isinstance(limits, dict) or set(limits) != AGENT_IDS:
        raise ConfigError("budgets: one limit per agent required")
    for name, limit in limits.items():
        if not isinstance(limit, dict):
            raise ConfigError(f"budgets: missing limits for {name}")
        _positive_integer(limit.get("monthly_token_limit"), f"{name}.monthly_token_limit")
        _positive_number(limit.get("monthly_usd_limit"), f"{name}.monthly_usd_limit")
        if limit["monthly_usd_limit"] != by_id[name]["monthly_budget_usd"]:
            raise ConfigError(f"{name}: USD budgets disagree across files")
    if sum(a["monthly_budget_usd"] for a in entries) > budgets["global_monthly_limit_usd"]:
        raise ConfigError("global budget smaller than per-agent sum")

    return {"agents": agents, "approvals": approvals, "budgets": budgets}
