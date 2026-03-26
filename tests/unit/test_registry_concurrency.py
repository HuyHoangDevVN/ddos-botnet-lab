import threading
import unittest

from orchestrator.session_registry import SessionRegistry


class TestRegistryConcurrency(unittest.TestCase):
    def test_register_and_heartbeat_concurrently(self):
        registry = SessionRegistry(max_agents=200)

        def worker(index: int):
            agent_id = f"agent-{index}"
            registry.register(agent_id, ["test"])
            registry.heartbeat(agent_id)

        threads = [threading.Thread(target=worker, args=(i,)) for i in range(50)]
        for thread in threads:
            thread.start()
        for thread in threads:
            thread.join()

        statuses = registry.list_status()
        self.assertEqual(len(statuses), 50)
        self.assertIn("agent-0", statuses)


if __name__ == "__main__":
    unittest.main()

