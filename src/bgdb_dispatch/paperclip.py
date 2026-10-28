"""Paperclip API адаптер; отдалеченият достъп изисква ограничен токен.

Не излагай помощника като публична HTTP услуга без удостоверяване.
"""
from __future__ import annotations

import json
import os
from urllib.error import HTTPError, URLError
from urllib.parse import quote, urlsplit
from urllib.request import Request, urlopen


class ConfigurationError(ValueError):
    pass


class PaperclipError(RuntimeError):
    pass


def validate_base_url(base_url: str) -> str:
    """Отхвърля незащитен HTTP и URL с потребител или параметри."""
    url = urlsplit(base_url)
    if not url.hostname or url.username or url.password or url.query or url.fragment or url.path not in ("", "/"):
        raise ConfigurationError("PAPERCLIP_BASE_URL must be a server origin (no path, userinfo, query or fragment)")
    host = url.hostname.casefold()
    if url.scheme == "https":
        return base_url.rstrip("/")
    if url.scheme == "http" and host in {"localhost", "127.0.0.1", "::1"}:
        return base_url.rstrip("/")
    raise ConfigurationError("Use HTTPS for remote Paperclip; HTTP is allowed only on loopback")


class PaperclipClient:
    def __init__(self, base_url: str | None = None, token: str | None = None, timeout: int = 15):
        self.base_url = validate_base_url(base_url or os.environ.get("PAPERCLIP_BASE_URL", "http://127.0.0.1:3100"))
        self.token = token if token is not None else os.environ.get("PAPERCLIP_TOKEN", "")
        if not self.token and urlsplit(self.base_url).hostname not in {"localhost", "127.0.0.1", "::1"}:
            raise ConfigurationError("PAPERCLIP_TOKEN is required for remote connections")
        self.timeout = timeout

    def request(self, method: str, path: str, payload: dict | None = None):
        headers = {"Accept": "application/json", "User-Agent": "BGDB-AI-EMDS/0.1.0"}
        if self.token:
            headers["Authorization"] = f"Bearer {self.token}"
        data = None
        if payload is not None:
            headers["Content-Type"] = "application/json"
            data = json.dumps(payload, ensure_ascii=False).encode("utf-8")
        req = Request(self.base_url + path, headers=headers, data=data, method=method)
        try:
            with urlopen(req, timeout=self.timeout) as response:
                body = response.read(1024 * 1024)
                return json.loads(body) if body else None
        except HTTPError as exc:
            detail = exc.read(300).decode("utf-8", "replace")
            raise PaperclipError(f"Paperclip HTTP {exc.code}: {detail}") from None
        except (URLError, TimeoutError, OSError) as exc:
            raise PaperclipError(f"Cannot reach Paperclip: {exc.reason if isinstance(exc, URLError) else exc}") from None

    def create_issue(self, company_id: str, issue: dict):
        return self.request("POST", f"/api/companies/{quote(company_id, safe='')}/issues", issue)

    def list_issues(self, company_id: str):
        return self.request("GET", f"/api/companies/{quote(company_id, safe='')}/issues?limit=25")

    def get_issue(self, issue_id: str):
        return self.request("GET", f"/api/issues/{quote(issue_id, safe='')}")
