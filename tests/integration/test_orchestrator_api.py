import os
import tempfile
import unittest

from core.config import LabConfig
from orchestrator.api import create_app


class TestOrchestratorAPI(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.NamedTemporaryFile(delete=False)
        self._tmp.close()
        cfg = LabConfig(audit_log_path=self._tmp.name)
        app = create_app(cfg)
        self.client = app.test_client()

    def tearDown(self):
        if os.path.exists(self._tmp.name):
            os.remove(self._tmp.name)

    def test_health(self):
        response = self.client.get("/api/health")
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.get_json()["simulate_only"])

    def test_scenario_listing(self):
        response = self.client.get("/api/scenarios")
        self.assertEqual(response.status_code, 200)
        body = response.get_json()
        self.assertIn("baseline", body["scenarios"])

    def test_scenario_metadata(self):
        response = self.client.get("/api/scenarios/baseline")
        self.assertEqual(response.status_code, 200)
        body = response.get_json()
        self.assertEqual(body["scenario"], "baseline")
        self.assertGreaterEqual(body["event_count"], 1)

    def test_rejects_invalid_command(self):
        payload = {"command": "bad", "agent_id": "agent-alpha", "issued_by": "tester"}
        response = self.client.post("/api/command", json=payload)
        self.assertEqual(response.status_code, 400)

    def test_accepts_ping(self):
        payload = {"command": "ping", "agent_id": "agent-alpha", "issued_by": "tester", "role": "operator"}
        response = self.client.post("/api/command", json=payload)
        self.assertEqual(response.status_code, 200)
        body = response.get_json()
        self.assertEqual(body["status"], "ok")
        self.assertTrue(body["events"])

    def test_replay_sdn_scenario(self):
        payload = {
            "command": "replay_detection_scenario",
            "agent_id": "agent-alpha",
            "issued_by": "tester",
            "role": "operator",
            "args": {"scenario": "sdn_flow_anomaly"},
        }
        response = self.client.post("/api/command", json=payload)
        self.assertEqual(response.status_code, 200)
        body = response.get_json()
        self.assertEqual(body["status"], "ok")
        self.assertGreaterEqual(len(body["events"]), 1)
        self.assertIn("event_type", body["events"][0])


if __name__ == "__main__":
    unittest.main()

