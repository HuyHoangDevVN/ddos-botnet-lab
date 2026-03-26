import unittest

from core.config import LabConfig
from core.safety import SafetyError, validate_config


class TestSafetyValidation(unittest.TestCase):
    def test_rejects_non_simulate_mode(self):
        cfg = LabConfig(simulate_only=False)
        with self.assertRaises(SafetyError):
            validate_config(cfg)

    def test_rejects_bind_outside_allowlist(self):
        cfg = LabConfig(bind_host="10.10.10.10", allowlisted_subnets=["127.0.0.0/8"])
        with self.assertRaises(SafetyError):
            validate_config(cfg)

    def test_accepts_default_safe_config(self):
        cfg = LabConfig()
        validate_config(cfg)


if __name__ == "__main__":
    unittest.main()

