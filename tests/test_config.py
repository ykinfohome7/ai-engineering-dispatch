"""Тестове на примерните YAML настройки и защитата срещу невалидни лимити."""

import json
import tempfile
import unittest
from pathlib import Path

from bgdb_dispatch.config import AGENT_IDS, ConfigError, load_config

CONFIG_DIR = Path(__file__).resolve().parents[1] / "config"


class ConfigTests(unittest.TestCase):
    """Проверява, че файловете са съгласувани и не разрешават безконтролни действия."""

    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        for filename in ("agents.yaml", "approvals.yaml", "budgets.yaml"):
            (self.root / filename).write_text(
                (CONFIG_DIR / filename).read_text(encoding="utf-8"), encoding="utf-8"
            )

    def edit(self, name, change):
        """Променя временен файл, без да засяга реалния репозиториум."""
        path = self.root / name
        payload = json.loads(path.read_text(encoding="utf-8"))
        change(payload)
        path.write_text(json.dumps(payload), encoding="utf-8")

    def test_valid_config_and_seven_agents(self):
        settings = load_config(self.root)
        self.assertEqual({x["id"] for x in settings["agents"]["agents"]}, AGENT_IDS)
        self.assertTrue(settings["budgets"]["placeholder_only"])

    def test_default_repository_config(self):
        self.assertEqual(len(load_config()["agents"]["agents"]), 7)

    def test_missing_file_rejected(self):
        (self.root / "budgets.yaml").unlink()
        with self.assertRaises(ConfigError):
            load_config(self.root)

    def test_non_json_yaml_subset_rejected(self):
        (self.root / "agents.yaml").write_text("agents: invalid\n", encoding="utf-8")
        with self.assertRaises(ConfigError):
            load_config(self.root)

    def test_unknown_agent_rejected(self):
        self.edit("agents.yaml", lambda d: d["agents"][0].update(id="unapproved"))
        with self.assertRaises(ConfigError):
            load_config(self.root)

    def test_duplicate_agent_rejected(self):
        self.edit("agents.yaml", lambda d: d["agents"][0].update(id="docs"))
        with self.assertRaises(ConfigError):
            load_config(self.root)

    def test_mismatched_budget_rejected(self):
        self.edit("budgets.yaml", lambda d: d["agents"]["architect"].update(monthly_usd_limit=999))
        with self.assertRaises(ConfigError):
            load_config(self.root)

    def test_zero_token_limit_rejected(self):
        self.edit("budgets.yaml", lambda d: d["agents"]["devops"].update(monthly_token_limit=0))
        with self.assertRaises(ConfigError):
            load_config(self.root)

    def test_unsafe_approval_default_rejected(self):
        self.edit("approvals.yaml", lambda d: d.update(default_decision="allow"))
        with self.assertRaises(ConfigError):
            load_config(self.root)

    def test_unknown_approval_rejected(self):
        self.edit("agents.yaml", lambda d: d["agents"][1]["needs_approval"].append("publish_secrets"))
        with self.assertRaises(ConfigError):
            load_config(self.root)

    def test_unaffordable_global_limit_rejected(self):
        self.edit("budgets.yaml", lambda d: d.update(global_monthly_limit_usd=1))
        with self.assertRaises(ConfigError):
            load_config(self.root)


if __name__ == "__main__":
    unittest.main()
