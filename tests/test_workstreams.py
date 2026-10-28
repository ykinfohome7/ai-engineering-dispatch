"""Проверки за седемте направления и безопасния dry-run."""
import importlib.util
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("register_workstreams", ROOT / "scripts" / "register-workstreams.py")
module = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(module)


class WorkstreamsTests(unittest.TestCase):
    """Никакви реални Paperclip заявки от тестовете."""

    def setUp(self):
        self.items = module.load_workstreams(ROOT / "config" / "workstreams.yaml")

    def test_seven_workstreams(self):
        self.assertEqual(len(self.items), 7)
        self.assertEqual(len({i["id"] for i in self.items}), 7)
        self.assertTrue(all(i["lead_agent"] != i["review_agent"] for i in self.items))

    def test_dry_run_is_offline(self):
        lines = []
        with patch.object(module, "request_projects", side_effect=AssertionError("Unexpected network")):
            module.register(self.items, apply=False, output=lines.append)
        self.assertEqual(len(lines), 8)

    def test_apply_needs_company_id(self):
        with self.assertRaises(ValueError):
            module.register(self.items, apply=True, company="", base="http://127.0.0.1:3100")

    def test_remote_http_rejected(self):
        with self.assertRaises(ValueError):
            module.normalized_url("http://example.com:3100", token="token")

    def test_existing_projects_are_not_duplicated(self):
        company = "11111111-2222-3333-4444-555555555555"
        exists = [{"id": str(n), "name": x["name"]} for n, x in enumerate(self.items)]
        with patch.object(module, "request_projects", return_value=exists) as api:
            module.register(self.items, apply=True, base="http://127.0.0.1:3100", company=company, output=lambda _: None)
            self.assertEqual(api.call_count, 1)

    def test_missing_projects_start_planned(self):
        company = "11111111-2222-3333-4444-555555555555"
        calls = []
        def fake(base, company, token, method, payload=None):
            calls.append((method, payload))
            return [] if method == "GET" else {"id": "new"}
        with patch.object(module, "request_projects", side_effect=fake):
            module.register(self.items, apply=True, base="http://127.0.0.1:3100", company=company, output=lambda _: None)
        self.assertEqual(len(calls), 8)
        self.assertTrue(all(c[1]["status"] == "planned" for c in calls[1:]))

    def test_duplicate_name_rejected(self):
        with tempfile.TemporaryDirectory() as temp:
            cfg = json.loads((ROOT / "config/workstreams.yaml").read_text())
            cfg["workstreams"][1]["name"] = cfg["workstreams"][0]["name"]
            path = Path(temp) / "workstreams.yaml"
            path.write_text(json.dumps(cfg))
            with self.assertRaises(ValueError):
                module.load_workstreams(path)


if __name__ == "__main__":
    unittest.main()
