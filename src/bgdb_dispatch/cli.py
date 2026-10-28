"""Прием на задачи към Paperclip, само при изрично --execute."""
from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path

from . import __version__
from .paperclip import ConfigurationError, PaperclipClient, PaperclipError
from .roles import ROLES, choose_role


def issue_payload(title: str, description: str, role: str, priority: str, project_id: str = "") -> dict:
    if not title.strip():
        raise ConfigurationError("Task title cannot be empty")
    if role not in ROLES:
        raise ConfigurationError(f"Unknown role: {role}")
    payload = {
        "title": title.strip(),
        "description": description.strip() + f"\n\n---\nBGDB AI-EMDS suggested role: **{ROLES[role]['name']}**.\nHuman review required before deployment.",
        "status": "todo",
        "priority": priority,
    }
    if project_id:
        payload["projectId"] = project_id
    agent_id = os.environ.get(f"PAPERCLIP_AGENT_{role.upper()}_ID", "").strip()
    if agent_id:
        payload["assigneeAgentId"] = agent_id
    return payload


def parser_factory() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="bgdb-dispatch", description="BGDB AI-EMDS Paperclip dispatcher")
    parser.add_argument("--version", action="version", version=__version__)
    sub = parser.add_subparsers(dest="command", required=True)
    sub.add_parser("roles", help="List roles and mapping keywords")
    p = sub.add_parser("plan", help="Preview a task without making network calls")
    p.add_argument("title")
    p.add_argument("--description", default="")
    p.add_argument("--description-file", type=Path)
    p.add_argument("--role", choices=list(ROLES))
    p.add_argument("--priority", choices=("urgent", "high", "medium", "low"), default="medium")
    p.add_argument("--project-id", default="")
    p = sub.add_parser("submit", help="Create Paperclip issue (--execute required)")
    p.add_argument("title")
    p.add_argument("--description", default="")
    p.add_argument("--description-file", type=Path)
    p.add_argument("--role", choices=list(ROLES))
    p.add_argument("--priority", choices=("urgent", "high", "medium", "low"), default="medium")
    p.add_argument("--project-id", default="")
    p.add_argument("--execute", action="store_true")
    sub.add_parser("doctor", help="Check Paperclip connection and credentials")
    sub.add_parser("list", help="List up to 25 Paperclip issues")
    p = sub.add_parser("get", help="Fetch one Paperclip issue")
    p.add_argument("issue_id")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = parser_factory().parse_args(argv)
    try:
        if args.command == "roles":
            result = {name: role["name"] for name, role in ROLES.items()}
        elif args.command in ("plan", "submit"):
            description = args.description
            if args.description_file:
                if description:
                    raise ConfigurationError("Use --description OR --description-file, not both")
                description = args.description_file.read_text(encoding="utf-8")
            role = args.role or choose_role(args.title + " " + description)
            result = issue_payload(args.title, description, role, args.priority, args.project_id)
            if args.command == "submit" and args.execute:
                company = os.environ.get("PAPERCLIP_COMPANY_ID", "").strip()
                if not company:
                    raise ConfigurationError("Set PAPERCLIP_COMPANY_ID before --execute")
                result = PaperclipClient().create_issue(company, result)
            elif args.command == "submit":
                print("DRY RUN: use --execute to create the Paperclip issue", file=sys.stderr)
        elif args.command in ("list", "doctor"):
            company = os.environ.get("PAPERCLIP_COMPANY_ID", "").strip()
            if not company:
                raise ConfigurationError("Set PAPERCLIP_COMPANY_ID first")
            result = PaperclipClient().list_issues(company)
            if args.command == "doctor":
                result = {"connected": True, "company_id": company}
        else:
            result = PaperclipClient().get_issue(args.issue_id)
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return 0
    except (ConfigurationError, PaperclipError, UnicodeError, OSError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
