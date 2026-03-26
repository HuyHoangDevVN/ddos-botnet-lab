import unittest

from core.config import LabConfig
from orchestrator.api import create_app


class TestKillSwitch(unittest.TestCase):
    def test_blocks_commands_when_kill_switch_is_active(self):
        cfg = LabConfig(kill_switch=True)
        app = create_app(cfg)
        client = app.test_client()

        payload = {"command": "ping", "agent_id": "agent-alpha", "issued_by": "tester"}
        response = client.post("/api/command", json=payload)
        self.assertEqual(response.status_code, 409)
        self.assertIn("Kill switch active", response.get_json()["error"])


if __name__ == "__main__":
    unittest.main()

