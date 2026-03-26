import json
from pathlib import Path
from typing import Dict, List

from observability.audit_logger import AuditLogger


class ReplayEngine:
    def __init__(self, dataset_dir: str, max_events: int):
        self._dataset_dir = Path(dataset_dir)
        self._max_events = max_events

    def list_scenarios(self) -> List[str]:
        scenarios: List[str] = []
        for path in sorted(self._dataset_dir.glob("*.jsonl")):
            scenarios.append(path.stem)
        return scenarios

    def scenario_metadata(self, scenario: str) -> Dict[str, str | int]:
        scenario_file = self._dataset_dir / f"{scenario}.jsonl"
        if not scenario_file.exists():
            raise FileNotFoundError(f"Scenario dataset not found: {scenario_file}")

        event_count = 0
        with open(scenario_file, "r", encoding="utf-8") as handle:
            for event_count, _ in enumerate(handle, start=1):
                pass

        return {
            "scenario": scenario,
            "dataset_file": str(scenario_file),
            "event_count": event_count,
            "max_replay_events": self._max_events,
        }

    def replay(self, scenario: str, audit: AuditLogger, correlation_id: str) -> List[Dict[str, str]]:
        scenario_file = self._dataset_dir / f"{scenario}.jsonl"
        if not scenario_file.exists():
            raise FileNotFoundError(f"Scenario dataset not found: {scenario_file}")

        events: List[Dict[str, str]] = []
        with open(scenario_file, "r", encoding="utf-8") as handle:
            for idx, line in enumerate(handle):
                if idx >= self._max_events:
                    break
                payload = json.loads(line)
                if not isinstance(payload, dict):
                    raise ValueError(f"Replay event must be an object (scenario={scenario}, index={idx})")
                if "event_type" not in payload:
                    raise ValueError(
                        f"Replay event missing event_type (scenario={scenario}, index={idx})"
                    )
                payload["correlation_id"] = correlation_id
                events.append(payload)
                audit.log(
                    "replay_event_emitted",
                    {
                        "correlation_id": correlation_id,
                        "scenario": scenario,
                        "event_index": idx,
                        "component": "replay_engine",
                    },
                )
        return events

