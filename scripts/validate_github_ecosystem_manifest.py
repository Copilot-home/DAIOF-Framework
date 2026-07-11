#!/usr/bin/env python3
"""Validate the Copilot-home ecosystem manifest using only Python stdlib."""

from __future__ import annotations

import json
import sys
from datetime import date
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "governance" / "github_ecosystem_manifest.json"

TOP_LEVEL_FIELDS = {
    "$schema",
    "schema_version",
    "org",
    "generated_at",
    "source_of_truth",
    "policy",
    "repositories",
}
POLICY = {
    "mutation_mode": "pull-request-only",
    "ci_authority_rule": "exactly-one-authoritative-gate-per-active-repository",
    "secret_policy": "no-secrets-in-repository",
    "public_path_policy": "no-absolute-local-paths-in-public-artifacts",
    "default_branch_rule": "main-unless-upstream-or-migration-exception-is-documented",
}
VISIBILITY = {"public", "private", "internal"}
NAMESPACES = {
    "core",
    "runtime",
    "tooling",
    "workbench",
    "product",
    "experiment",
    "reference",
    "archive",
}
LIFECYCLES = {
    "active",
    "incubating",
    "maintenance",
    "needs-normalization",
    "archive-candidate",
    "empty",
}
CI_AUTHORITIES = {
    "local-verifier",
    "github-actions",
    "circleci",
    "upstream",
    "none",
    "undetermined",
}
QUOTA_LEVELS = {"low", "medium", "high"}
EVIDENCE = {"verified-by-github-connector", "partial", "missing"}

REQUIRED_REPO_FIELDS = {
    "name",
    "visibility",
    "size_kb",
    "default_branch",
    "namespace",
    "role",
    "lifecycle",
    "ci_authority",
    "ci_secondary",
    "local_first",
    "local_artifacts_allowed",
    "secret_policy",
    "quota_criticality",
    "normalization_flags",
    "evidence_status",
    "last_verified_at",
}
OPTIONAL_REPO_FIELDS = {"default_branch_exception"}
ALLOWED_REPO_FIELDS = REQUIRED_REPO_FIELDS | OPTIONAL_REPO_FIELDS
BRANCH_EXCEPTION_FIELDS = {"owner", "rationale", "exit_criteria", "rollback"}


def fail(message: str) -> None:
    raise ValueError(message)


def require(condition: bool, message: str) -> None:
    if not condition:
        fail(message)


def validate_date(value: Any, field: str) -> None:
    require(isinstance(value, str), f"{field} must be an ISO date string")
    try:
        parsed = date.fromisoformat(value)
    except ValueError as exc:
        raise ValueError(f"{field} must use YYYY-MM-DD") from exc
    require(parsed.isoformat() == value, f"{field} must use canonical YYYY-MM-DD")


def validate_string_list(value: Any, field: str) -> None:
    require(
        isinstance(value, list) and all(isinstance(item, str) and item for item in value),
        f"{field} must be a list of non-empty strings",
    )
    require(len(value) == len(set(value)), f"{field} contains duplicates")


def validate_branch_exception(repo: dict[str, Any], name: str) -> None:
    exception = repo.get("default_branch_exception")
    if repo["default_branch"] == "main":
        return

    require(
        isinstance(exception, dict),
        f"{name}: non-main branch requires default_branch_exception",
    )
    missing = BRANCH_EXCEPTION_FIELDS - exception.keys()
    extra = exception.keys() - BRANCH_EXCEPTION_FIELDS
    require(
        not missing,
        f"{name}: default_branch_exception missing fields: {sorted(missing)}",
    )
    require(
        not extra,
        f"{name}: default_branch_exception has unexpected fields: {sorted(extra)}",
    )
    for field in sorted(BRANCH_EXCEPTION_FIELDS):
        value = exception[field]
        require(
            isinstance(value, str) and value.strip(),
            f"{name}: default_branch_exception.{field} invalid",
        )


def validate_repo(repo: dict[str, Any], index: int) -> None:
    missing = REQUIRED_REPO_FIELDS - repo.keys()
    extra = repo.keys() - ALLOWED_REPO_FIELDS
    require(not missing, f"repositories[{index}] missing fields: {sorted(missing)}")
    require(not extra, f"repositories[{index}] unexpected fields: {sorted(extra)}")

    name = repo["name"]
    require(
        isinstance(name, str) and name.strip(),
        f"repositories[{index}].name invalid",
    )
    require(repo["visibility"] in VISIBILITY, f"{name}: invalid visibility")
    require(
        isinstance(repo["size_kb"], int) and repo["size_kb"] >= 0,
        f"{name}: invalid size_kb",
    )
    require(
        isinstance(repo["default_branch"], str) and repo["default_branch"],
        f"{name}: invalid default_branch",
    )
    require(repo["namespace"] in NAMESPACES, f"{name}: invalid namespace")
    require(isinstance(repo["role"], str) and repo["role"], f"{name}: invalid role")
    require(repo["lifecycle"] in LIFECYCLES, f"{name}: invalid lifecycle")
    require(
        repo["ci_authority"] in CI_AUTHORITIES,
        f"{name}: invalid ci_authority",
    )
    require(
        isinstance(repo["local_first"], bool),
        f"{name}: local_first must be boolean",
    )
    require(
        isinstance(repo["local_artifacts_allowed"], bool),
        f"{name}: local_artifacts_allowed must be boolean",
    )
    require(
        repo["secret_policy"] == "no-secrets-in-repository",
        f"{name}: secret policy drift",
    )
    require(
        repo["quota_criticality"] in QUOTA_LEVELS,
        f"{name}: invalid quota_criticality",
    )
    require(
        repo["evidence_status"] in EVIDENCE,
        f"{name}: invalid evidence_status",
    )
    validate_date(repo["last_verified_at"], f"{name}.last_verified_at")
    validate_string_list(
        repo["normalization_flags"],
        f"{name}.normalization_flags",
    )
    validate_string_list(repo["ci_secondary"], f"{name}.ci_secondary")
    require(
        repo["ci_authority"] not in repo["ci_secondary"],
        f"{name}: ci_authority must not be repeated in ci_secondary",
    )

    if repo["visibility"] == "public":
        require(
            not repo["local_artifacts_allowed"],
            f"{name}: public repositories cannot allow local artifacts",
        )

    if repo["lifecycle"] == "active":
        require(
            repo["ci_authority"] not in {"none", "undetermined"},
            f"{name}: active lifecycle requires a declared CI authority",
        )

    if repo["lifecycle"] == "empty":
        require(
            repo["size_kb"] == 0,
            f"{name}: empty lifecycle requires size_kb=0",
        )
        require(
            repo["ci_authority"] == "none",
            f"{name}: empty lifecycle requires ci_authority=none",
        )

    validate_branch_exception(repo, name)


def validate_manifest(data: dict[str, Any]) -> dict[str, Any]:
    missing = TOP_LEVEL_FIELDS - data.keys()
    extra = data.keys() - TOP_LEVEL_FIELDS
    require(not missing, f"manifest missing fields: {sorted(missing)}")
    require(not extra, f"manifest unexpected fields: {sorted(extra)}")

    require(
        data["$schema"] == "./github_ecosystem_manifest.schema.json",
        "$schema pointer drift",
    )
    require(data["schema_version"] == "1.1.0", "schema_version must be 1.1.0")
    require(data["org"] == "Copilot-home", "org must be Copilot-home")
    validate_date(data["generated_at"], "generated_at")
    require(
        data["source_of_truth"] == "github:Copilot-home/DAIOF-Framework",
        "source_of_truth drift",
    )
    require(data["policy"] == POLICY, "policy block drift")

    repos = data["repositories"]
    require(isinstance(repos, list), "repositories must be a list")
    require(len(repos) == 18, f"expected 18 repositories, found {len(repos)}")

    names: set[str] = set()
    for index, repo in enumerate(repos):
        require(
            isinstance(repo, dict),
            f"repositories[{index}] must be an object",
        )
        validate_repo(repo, index)
        name = repo["name"]
        require(name not in names, f"duplicate repository name: {name}")
        names.add(name)

    return {
        "status": "PASS",
        "org": data["org"],
        "repository_count": len(repos),
        "source_of_truth": data["source_of_truth"],
        "schema_version": data["schema_version"],
    }


def main() -> int:
    data = json.loads(MANIFEST.read_text(encoding="utf-8"))
    print(json.dumps(validate_manifest(data), ensure_ascii=False))
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (OSError, json.JSONDecodeError, ValueError) as exc:
        print(
            json.dumps({"status": "FAIL", "error": str(exc)}, ensure_ascii=False),
            file=sys.stderr,
        )
        raise SystemExit(1)
