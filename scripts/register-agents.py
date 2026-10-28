#!/usr/bin/env python3
"""Dry-run или изрична регистрация на седем агента в Paperclip."""
from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
import re
import sys
from urllib.parse import urlsplit
from urllib.request import Request, urlopen
from urllib.error import HTTPError, URLError

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from bgdb_dispatch.config import load_config, ConfigError  # noqa: E402

# Реалните Paperclip роли и adapterType се различават от BGDB етикетите.
ROLE = {
    "architect": "cto", "developer-claude-code": "engineer",
    "developer-codex": "engineer", "reviewer": "security",
    "qa-tester": "qa", "devops": "devops", "docs": "general",
}
ADAPTER = {
    key: ("codex_local" if key in {"developer-codex", "qa-tester"} else "claude_local")
    for key in ROLE
}
UUID = re.compile(r"[0-9a-fA-F]{8}(?:-[0-9a-fA-F]{4}){3}-[0-9a-fA-F]{12}\Z")


def agent_payload(agent: dict, budget: dict) -> dict:
    """Подготвя запис с месечен USD таван, без ключове и пароли."""
    aid = agent["id"]
    return {
        "name": f"BGDB - {aid}",
        "role": ROLE[aid],
        "title": agent["role"],
        "capabilities": ", ".join(agent["allowed_actions"]),
        "adapterType": ADAPTER[aid],
        "adapterConfig": {},
        "budgetMonthlyCents": round(budget["monthly_usd_limit"] * 100),
        "metadata": {"bgdbConfigAgentId": aid},
    }


def validate_url(base_url: str, token: str) -> str:
    """Блокира отдалечени HTTP адреси и URL със секрети."""
    parts = urlsplit(base_url)
    if parts.scheme not in {"http", "https"} or not parts.hostname or parts.username or parts.password:
        raise ValueError("Invalid Paperclip URL")
    if parts.path not in {"", "/"} or parts.query or parts.fragment:
        raise ValueError("Paperclip URL must be a host root")
    if parts.scheme == "http" and parts.hostname not in {"127.0.0.1", "localhost", "::1"}:
        raise ValueError("Remote Paperclip requires HTTPS")
    if parts.hostname not in {"127.0.0.1", "localhost", "::1"} and not token:
        raise ValueError("Remote Paperclip requires a token")
    return base_url.rstrip("/")


def api_request(base: str, company: str, token: str, method: str, payload: dict | None = None):
    """Изпълнява само GET/POST; не показва токена или API грешки с лични данни."""
    headers = {"Accept": "application/json"}
    if token:
        headers["Authorization"] = "Bearer " + token
    body = None
    if payload is not None:
        headers["Content-Type"] = "application/json"
        body = json.dumps(payload).encode("utf-8")
    req = Request(f"{base}/api/companies/{company}/agents", data=body, headers=headers, method=method)
    try:
        with urlopen(req, timeout=12) as response:
            return json.load(response)
    except HTTPError as exc:
        raise RuntimeError(f"Paperclip API HTTP {exc.code}; inspect before retrying") from None
    except (URLError, TimeoutError):
        raise RuntimeError("Cannot reach Paperclip; check authorization and access") from None


def register(settings: dict, base: str, company: str, token: str, *, apply: bool, output=print) -> int:
    """Проверява всички бюджетни конфликти преди създаване; без дубликати."""
    entries = settings["agents"]["agents"]
    budgets = settings["budgets"]["agents"]
    if not apply:
        for agent in entries:
            payload = agent_payload(agent, budgets[agent["id"]])
            output(f'DRY-RUN {payload["name"]}: {payload["adapterType"]}, USD {payload["budgetMonthlyCents"]/100:.2f}/month')
        output("No API calls. Placeholder budgets and approvals are not active policy.")
        return 0
    if not UUID.fullmatch(company):
        raise ValueError("PAPERCLIP_COMPANY_ID must be a UUID")
    base = validate_url(base, token)
    current = api_request(base, company, token, "GET")
    if isinstance(current, dict):
        current = current.get("agents")
    if not isinstance(current, list):
        raise RuntimeError("Unexpected Paperclip response; stopped before writes")
    named = {a.get("name"): a for a in current if isinstance(a, dict)}
    for agent in entries:
        payload = agent_payload(agent, budgets[agent["id"]])
        existing = named.get(payload["name"])
        if existing and existing.get("budgetMonthlyCents") != payload["budgetMonthlyCents"]:
            raise RuntimeError(f'Budget differs for {payload["name"]}; review manually')
    for agent in entries:
        payload = agent_payload(agent, budgets[agent["id"]])
        if payload["name"] in named:
            output(f'EXISTS {payload["name"]}')
            continue
        created = api_request(base, company, token, "POST", payload)
        if not isinstance(created, dict) or not created.get("id"):
            raise RuntimeError(f'Creation not confirmed: {payload["name"]}; inspect before retrying')
        named[payload["name"]] = created
        output(f'CREATED {payload["name"]}')
    output("Records created. Configure and verify adapters, approvals and token limits manually.")
    return 0


def main(argv=None) -> int:
    """Без --apply само показва плана и не прави заявки."""
    parser = argparse.ArgumentParser(description="BGDB agent registration (dry-run default)")
    parser.add_argument("--apply", action="store_true")
    parser.add_argument("--config-dir", type=Path, default=ROOT / "config")
    args = parser.parse_args(argv)
    try:
        settings = load_config(args.config_dir)
        return register(
            settings,
            os.environ.get("PAPERCLIP_BASE_URL", "http://127.0.0.1:3100"),
            os.environ.get("PAPERCLIP_COMPANY_ID", ""),
            os.environ.get("PAPERCLIP_TOKEN", ""),
            apply=args.apply,
        )
    except (ConfigError, ValueError, RuntimeError) as exc:
        print(f"Registration stopped: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
