# Test Guide

Run all tests:

- `python -m unittest discover -s tests -v`

## Test Groups

- `tests/unit/`: schema, safety, audit logging, registry concurrency
- `tests/integration/`: orchestrator API workflow
- `tests/safety/`: kill-switch behavior

Expected result: all tests pass with safe defaults.
