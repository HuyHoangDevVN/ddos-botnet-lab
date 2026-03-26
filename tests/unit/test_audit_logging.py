import json
import os
import tempfile
import unittest

from observability.audit_logger import AuditLogger


class TestAuditLogging(unittest.TestCase):
    def test_writes_structured_log_with_expected_fields(self):
        temp = tempfile.NamedTemporaryFile(delete=False)
        temp.close()
        try:
            logger = AuditLogger(temp.name)
            logger.log(
                "command_received",
                {
                    "correlation_id": "cid-1",
                    "command": "ping",
                    "issued_by": "tester",
                },
            )
            with open(temp.name, "r", encoding="utf-8") as handle:
                line = handle.readline()
            payload = json.loads(line)
            self.assertEqual(payload["event_type"], "command_received")
            self.assertEqual(payload["correlation_id"], "cid-1")
            self.assertEqual(payload["command"], "ping")
            self.assertIn("timestamp", payload)
        finally:
            if os.path.exists(temp.name):
                os.remove(temp.name)


if __name__ == "__main__":
    unittest.main()

