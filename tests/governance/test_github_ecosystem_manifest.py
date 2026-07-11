from __future__ import annotations

import copy
import importlib.util
import json
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]
VALIDATOR_PATH = ROOT / "scripts" / "validate_github_ecosystem_manifest.py"
MANIFEST_PATH = ROOT / "governance" / "github_ecosystem_manifest.json"

spec = importlib.util.spec_from_file_location(
    "validate_github_ecosystem_manifest",
    VALIDATOR_PATH,
)
assert spec and spec.loader
validator = importlib.util.module_from_spec(spec)
spec.loader.exec_module(validator)


def load_manifest() -> dict:
    return json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))


def test_checked_in_manifest_passes() -> None:
    result = validator.validate_manifest(load_manifest())
    assert result["status"] == "PASS"
    assert result["repository_count"] == 18
    assert result["schema_version"] == "1.1.0"


@pytest.mark.parametrize(
    ("mutator", "message"),
    [
        (
            lambda data: data.__setitem__("generated_at", "11-07-2026"),
            "generated_at must use YYYY-MM-DD",
        ),
        (
            lambda data: data["policy"].pop("secret_policy"),
            "policy block drift",
        ),
        (
            lambda data: data["repositories"][0].__setitem__("unexpected", True),
            "unexpected fields",
        ),
    ],
)
def test_manifest_rejects_invalid_topology(mutator, message: str) -> None:
    data = copy.deepcopy(load_manifest())
    mutator(data)
    with pytest.raises(ValueError, match=message):
        validator.validate_manifest(data)


def test_non_main_branch_requires_structured_exception() -> None:
    data = copy.deepcopy(load_manifest())
    repo = next(item for item in data["repositories"] if item["name"] == "HyperAI-Sync")
    repo.pop("default_branch_exception")
    with pytest.raises(ValueError, match="non-main branch requires"):
        validator.validate_manifest(data)


def test_active_repo_requires_declared_ci_authority() -> None:
    data = copy.deepcopy(load_manifest())
    repo = next(item for item in data["repositories"] if item["name"] == "literate-robot")
    repo["ci_authority"] = "undetermined"
    with pytest.raises(ValueError, match="active lifecycle requires"):
        validator.validate_manifest(data)
