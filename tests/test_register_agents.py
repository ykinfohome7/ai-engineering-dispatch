"""Тестове без реални HTTP заявки за регистрацията на агенти."""
import importlib.util
import io
from pathlib import Path
import unittest
from unittest.mock import patch

from bgdb_dispatch.config import load_config

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("bgdb_agent_registry", ROOT / "scripts/register-agents.py")
registry = importlib.util.module_from_spec(spec)
spec.loader.exec_module(registry)


class RegistrationTests(unittest.TestCase):
    """Проверява dry-run, дубликати, лимити и безопасен URL."""

    def setUp(self):
        self.settings = load_config(ROOT / "config")
        self.company = "00000000-0000-4000-8000-000000000001"

    def test_preview_no_http_and_seven_roles(self):
        output = []
        with patch.object(registry, "api_request") as api:
            self.assertEqual(registry.register(self.settings, "", "", "", apply=False, output=output.append), 0)
            api.assert_not_called()
        self.assertEqual(sum(s.startswith("DRY-RUN") for s in output), 7)

    def test_payload_budget_and_roles(self):
        for agent in self.settings["agents"]["agents"]:
            payload = registry.agent_payload(agent, self.settings["budgets"]["agents"][agent["id"]])
            self.assertGreater(payload["budgetMonthlyCents"], 0)
            self.assertIn(payload["adapterType"], {"claude_local", "codex_local"})
            self.assertNotIn("token", payload)

    def test_remote_http_blocked(self):
        with self.assertRaises(ValueError):
            registry.validate_url("http://remote.example", "irrelevant")

    def test_remote_https_needs_token(self):
        with self.assertRaises(ValueError):
            registry.validate_url("https://remote.example", "")
        self.assertEqual(registry.validate_url("https://remote.example/", "irrelevant"), "https://remote.example")

    def test_invalid_company_rejected_before_network(self):
        with patch.object(registry, "api_request") as api, self.assertRaises(ValueError):
            registry.register(self.settings, "http://localhost:3100", "not-a-uuid", "", apply=True)
        api.assert_not_called()

    def test_apply_idempotent_seven_records(self):
        records = []
        verbs = []

        def fake_api(base, company, token, method, payload=None):
            verbs.append(method)
            if method == "GET":
                return list(records)
            result = dict(payload, id=f"a{len(records) + 1}")
            records.append(result)
            return result

        with patch.object(registry, "api_request", side_effect=fake_api):
            for _ in range(2):
                self.assertEqual(registry.register(self.settings, "http://localhost:3100", self.company, "", apply=True, output=lambda _: None), 0)
        self.assertEqual(verbs.count("POST"), 7)
        self.assertEqual(verbs.count("GET"), 2)

    def test_budget_conflict_stops_before_posts(self):
        with patch.object(registry, "api_request", return_value=[{"name": "BGDB - architect", "budgetMonthlyCents": 1}]) as api:
            with self.assertRaises(RuntimeError):
                registry.register(self.settings, "http://localhost:3100", self.company, "", apply=True)
        self.assertEqual(api.call_count, 1)

    def test_invalid_response_rejected(self):
        with patch.object(registry, "api_request", return_value={"wrong": []}) as api:
            with self.assertRaises(RuntimeError):
                registry.register(self.settings, "http://localhost:3100", self.company, "", apply=True)
        self.assertEqual(api.call_count, 1)

    def test_main_dry_run_needs_no_credentials(self):
        out = io.StringIO()
        with patch.dict(registry.os.environ, {}, clear=True), patch.object(registry, "api_request") as api, patch("sys.stdout", out):
            self.assertEqual(registry.main([]), 0)
            api.assert_not_called()
        self.assertIn("No API calls", out.getvalue())


if __name__ == "__main__":
    unittest.main()
