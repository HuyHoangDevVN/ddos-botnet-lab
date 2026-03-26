import os
import tempfile
import unittest

from observability.audit_logger import AuditLogger
from simulator.telemetry.replay_engine import ReplayEngine


class TestReplayEngine(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.log = tempfile.NamedTemporaryFile(delete=False)
        self.log.close()
        self.engine = ReplayEngine(self.temp_dir.name, max_events=10)
        self.audit = AuditLogger(self.log.name)

    def tearDown(self):
        if os.path.exists(self.log.name):
            os.remove(self.log.name)
        self.temp_dir.cleanup()

    def test_lists_scenarios(self):
        path = os.path.join(self.temp_dir.name, "scenario-a.jsonl")
        with open(path, "w", encoding="utf-8") as handle:
            handle.write('{"event_type":"x"}\n')
        scenarios = self.engine.list_scenarios()
        self.assertEqual(scenarios, ["scenario-a"])

    def test_rejects_event_without_type(self):
        path = os.path.join(self.temp_dir.name, "bad.jsonl")
        with open(path, "w", encoding="utf-8") as handle:
            handle.write('{"not_event_type":"x"}\n')
        with self.assertRaises(ValueError):
            self.engine.replay("bad", self.audit, "cid-1")


if __name__ == "__main__":
    unittest.main()

