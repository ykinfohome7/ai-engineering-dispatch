import contextlib
import io
import json
import os
import unittest
from unittest.mock import patch

from bgdb_dispatch.cli import main, issue_payload
from bgdb_dispatch.paperclip import ConfigurationError, PaperclipClient, validate_base_url
from bgdb_dispatch.roles import ROLES, choose_role


class RoleTests(unittest.TestCase):
    def test_role_registry(self):
        self.assertEqual(len(ROLES), 7)

    def test_routing(self):
        self.assertEqual(choose_role("deploy Tailscale server"), "devops")
        self.assertEqual(choose_role("Add regression tests"), "qa")
        self.assertEqual(choose_role("Write documentation manual"), "docs")
        self.assertEqual(choose_role("random request"), "architect")
        self.assertEqual(choose_role("Codex implement feature"), "developer_codex")

    def test_codex_agent_assignment(self):
        with patch.dict(os.environ, {"PAPERCLIP_AGENT_DEVELOPER_CODEX_ID": "codex-agent"}):
            self.assertEqual(issue_payload("task", "", "developer_codex", "medium")["assigneeAgentId"], "codex-agent")

    def test_assignee_not_included_unless_configured(self):
        with patch.dict(os.environ, {}, clear=True):
            self.assertNotIn("assigneeAgentId", issue_payload("some task", "", "developer", "low"))
        with patch.dict(os.environ, {"PAPERCLIP_AGENT_DEVELOPER_ID": "abc"}):
            self.assertEqual(issue_payload("task", "", "developer", "high")["assigneeAgentId"], "abc")


class SecurityTests(unittest.TestCase):
    def test_reject_insecure_remote(self):
        for url in ("http://example.com:3100", "https://x.com/path", "https://user:pass@x.com", "file:///tmp/x"):
            with self.subTest(url=url), self.assertRaises(ConfigurationError):
                validate_base_url(url)

    def test_allow_loopback(self):
        self.assertEqual(validate_base_url("http://127.0.0.1:3100/"), "http://127.0.0.1:3100")

    def test_remote_requires_token(self):
        with patch.dict(os.environ, {}, clear=True):
            with self.assertRaises(ConfigurationError):
                PaperclipClient("https://paperclip.example.com")


class CliTests(unittest.TestCase):
    def test_dry_run_never_posts(self):
        output = io.StringIO()
        with patch("bgdb_dispatch.cli.PaperclipClient") as client, contextlib.redirect_stdout(output), contextlib.redirect_stderr(io.StringIO()):
            self.assertEqual(main(["submit", "Deploy Tailscale and KSSH"]), 0)
            client.assert_not_called()
        self.assertEqual(json.loads(output.getvalue())["status"], "todo")

    def test_live_submit_requires_company_id(self):
        with patch.dict(os.environ, {}, clear=True), contextlib.redirect_stderr(io.StringIO()):
            self.assertEqual(main(["submit", "Task", "--execute"]), 1)

    def test_execute_posts_expected_payload(self):
        with patch.dict(os.environ, {"PAPERCLIP_COMPANY_ID": "company-1"}), patch("bgdb_dispatch.cli.PaperclipClient") as client, contextlib.redirect_stdout(io.StringIO()):
            client.return_value.create_issue.return_value = {"id": "issue-1"}
            self.assertEqual(main(["submit", "Add a Python API", "--execute", "--role", "developer"]), 0)
            args, kwargs = client.return_value.create_issue.call_args
            self.assertEqual(args[0], "company-1")
            self.assertEqual(args[1]["status"], "todo")


if __name__ == "__main__":
    unittest.main()
