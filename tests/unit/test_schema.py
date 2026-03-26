import unittest

from core.schemas import parse_command
from core.types import SafeCommand


class TestCommandSchema(unittest.TestCase):
    def test_rejects_unsupported_command(self):
        with self.assertRaises(ValueError):
            parse_command(
                {"command": "unknown", "agent_id": "agent-alpha", "issued_by": "tester"}
            )

    def test_parses_valid_payload(self):
        envelope = parse_command(
            {"command": "ping", "agent_id": "agent-alpha", "issued_by": "tester"}
        )
        self.assertEqual(envelope.command, SafeCommand.PING)
        self.assertEqual(envelope.agent_id, "agent-alpha")


if __name__ == "__main__":
    unittest.main()

