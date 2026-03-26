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


if __name__ == "__main__":
    unittest.main()

