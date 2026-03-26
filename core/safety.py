from core.config import LabConfig


class SafetyError(RuntimeError):
    pass


def consent_banner() -> str:
    return (
        "SAFE-LAB SIMULATOR\n"
        "This system is simulation-only and intended for defensive training.\n"
        "Unauthorized or non-lab use is prohibited."
    )


def validate_config(config: LabConfig) -> None:
    if not config.simulate_only:
        raise SafetyError("SIMULATE_ONLY must remain true for this repository.")
    if not config.bind_in_allowlist():
        raise SafetyError("BIND_HOST is not inside ALLOWLISTED_SUBNETS.")
    if config.max_commands_per_minute <= 0:
        raise SafetyError("MAX_COMMANDS_PER_MINUTE must be greater than 0.")
    if config.max_agents <= 0:
        raise SafetyError("MAX_AGENTS must be greater than 0.")
    if config.max_replay_events <= 0:
        raise SafetyError("MAX_REPLAY_EVENTS must be greater than 0.")

