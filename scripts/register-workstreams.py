#!/usr/bin/env python3
"""Създава само планирани проекти при изрично --apply."""
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
UUID = re.compile(r"[0-9a-fA-F]{8}(?:-[0-9a-fA-F]{4}){3}-[0-9a-fA-F]{12}\Z")
ROLES = {"architect", "developer-claude-code", "developer-codex", "reviewer", "qa-tester", "devops", "docs"}


def load_workstreams(path: Path) -> list[dict]:
    """Чете JSON-подмножество на YAML и проверява независимия преглед."""
    try:
        cfg = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        raise ValueError("Invalid workstreams configuration") from exc
    if not isinstance(cfg, dict) or cfg.get("version") != 1 or cfg.get("placeholder_only") is not True:
        raise ValueError("Expected version-1 templates")
    if cfg.get("projects_start_status") != "planned" or cfg.get("agent_execution") != "disabled_until_credentials_and_approvals_verified":
        raise ValueError("Unsafe project/agent policy")
    items = cfg.get("workstreams")
    if not isinstance(items, list) or len(items) != 7:
        raise ValueError("Exactly seven workstreams are required")
    names, ids = set(), set()
    for item in items:
        if not isinstance(item, dict):
            raise ValueError("Invalid workstream entry")
        name, identifier = item.get("name"), item.get("id")
        if not isinstance(name, str) or not name.strip() or name in names:
            raise ValueError("Duplicate or missing name")
        if not isinstance(identifier, str) or not identifier.strip() or identifier in ids:
            raise ValueError("Duplicate or missing identifier")
        if item.get("lead_agent") not in ROLES or item.get("review_agent") not in ROLES:
            raise ValueError("Invalid role")
        if item["lead_agent"] == item["review_agent"]:
            raise ValueError("Reviewer must be independent")
        cs = item.get("contributors")
        if not isinstance(cs, list) or not cs or not all(c in ROLES for c in cs):
            raise ValueError("Invalid contributors")
        if not isinstance(item.get("description"), str) or not item["description"].strip():
            raise ValueError("Description required")
        names.add(name)
        ids.add(identifier)
    return items


def normalized_url(url: str, token: str) -> str:
    """Блокира URL с тайни и отдалечен нешифрован HTTP."""
    parts = urlsplit(url)
    if parts.scheme not in {"http", "https"} or not parts.hostname or parts.username or parts.password or parts.path not in {"", "/"} or parts.query or parts.fragment:
        raise ValueError("Invalid Paperclip URL")
    if parts.scheme == "http" and parts.hostname not in {"127.0.0.1", "localhost", "::1"}:
        raise ValueError("Remote Paperclip requires HTTPS")
    if parts.hostname not in {"127.0.0.1", "localhost", "::1"} and not token:
        raise ValueError("Remote Paperclip requires authentication")
    return url.rstrip("/")


def request_projects(base: str, company: str, token: str, method: str, payload: dict | None = None):
    """Изпраща GET/POST и не извежда отговори с лични данни."""
    headers = {"Accept": "application/json"}
    if token:
        headers["Authorization"] = "Bearer " + token
    raw = None
    if payload is not None:
        headers["Content-Type"] = "application/json"
        raw = json.dumps(payload).encode("utf-8")
    req = Request(f"{base}/api/companies/{company}/projects", data=raw, method=method, headers=headers)
    try:
        with urlopen(req, timeout=15) as response:
            return json.load(response)
    except HTTPError as error:
        raise RuntimeError(f"Paperclip HTTP {error.code}") from None
    except (URLError, TimeoutError):
        raise RuntimeError("Paperclip connection failed") from None


def register(items: list[dict], *, apply: bool, base: str = "", company: str = "", token: str = "", output=print) -> int:
    """Проверява за дублиране и създава само статус planned."""
    if not apply:
        for item in items:
            output(f'PLAN {item["name"]}: lead={item["lead_agent"]}, reviewer={item["review_agent"]}, status=planned')
        output("DRY-RUN: no API requests, no agent execution.")
        return 0
    if not UUID.fullmatch(company):
        raise ValueError("PAPERCLIP_COMPANY_ID must be a UUID")
    base = normalized_url(base, token)
    current = request_projects(base, company, token, "GET")
    if isinstance(current, dict):
        current = current.get("projects")
    if not isinstance(current, list):
        raise RuntimeError("Unexpected Paperclip project list")
    known = {p.get("name") for p in current if isinstance(p, dict)}
    for item in items:
        if item["name"] in known:
            output(f'EXISTS {item["name"]}')
            continue
        created = request_projects(base, company, token, "POST", {
            "name": item["name"],
            "description": item["description"],
            "status": "planned",
        })
        if not isinstance(created, dict) or not created.get("id"):
            raise RuntimeError(f'Creation unconfirmed for {item["name"]}')
        known.add(item["name"])
        output(f'CREATED {item["name"]}')
    output("Planned projects created; agents remain inactive.")
    return 0


def main(argv=None) -> int:
    """При липса на --apply няма мрежови заявки."""
    parser = argparse.ArgumentParser(description="Paperclip workstreams; dry run by default")
    parser.add_argument("--apply", action="store_true")
    parser.add_argument("--config", type=Path, default=ROOT / "config" / "workstreams.yaml")
    args = parser.parse_args(argv)
    try:
        return register(
            load_workstreams(args.config),
            apply=args.apply,
            base=os.environ.get("PAPERCLIP_BASE_URL", "http://127.0.0.1:3100"),
            company=os.environ.get("PAPERCLIP_COMPANY_ID", ""),
            token=os.environ.get("PAPERCLIP_TOKEN", ""),
        )
    except (ValueError, RuntimeError) as exc:
        print(f"Workstream registration stopped: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
