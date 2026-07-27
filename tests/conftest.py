"""Test fixtures and mocks for HyperAI app.py."""

import sys
from types import ModuleType


def _mock_hypercore() -> None:
    """Provide a minimal fake hypercore module so app.py can be imported without the workbench path."""
    if "hypercore" in sys.modules:
        return

    hypercore = ModuleType("hypercore")

    class _ExecutionMode:
        def __init__(self, value):
            self.value = value

    class ExecutionMode:
        READ_ONLY = _ExecutionMode("readOnly")

    class HyperCore:
        def __init__(self, mode=None):
            self.mode = mode

        def analyze_dict(self, metadata, source):
            return MockReport()

    class MockReport:
        compliance_status = "OK"
        timestamp = "2026-07-27T00:00:00"

        def to_dict(self):
            return {"compliance_status": self.compliance_status, "timestamp": self.timestamp}

    hypercore.ExecutionMode = ExecutionMode
    hypercore.HyperCore = HyperCore
    sys.modules["hypercore"] = hypercore


_mock_hypercore()
