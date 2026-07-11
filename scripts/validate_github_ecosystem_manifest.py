#!/usr/bin/env python3
"""Validate the Copilot-home ecosystem manifest using only Python stdlib."""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "governance" / "github_ecosystem_manifest.json"

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
    "local_first",
    "local_artifacts_allowed",
    "secret_policy",
    "quota_criticality",
    "evidence_status",
    "last_verified_at",
}


def fail(message: str) -> None:
    raise ValueError(message)


def require(condition: bool, message: str) -> None:
    if not condition:
        fail(message)


def validate_repo(repo: dict[str, Any], index: int) -> None:
    missing = REQUIRED_REPO_FIELDS - repo.keys()
    require(not missing, f"repositories[{index}] missing fields: {sorted(missing)}")

    name = repo["name"]
    require(isinstance(name, str) and name.strip(), f"repositories[{index}].name invalid")
    require(repo["visibility"] in VISIBILITY, f"{name}: invalid visibility")
    require(isinstance(repo["size_kb"], int) and repo["size_kb"] >= 0, f"{name}: invalid size_kb")
    require(isinstance(repo["default_branch"], str) and repo["default_branch"], f"{name}: invalid default_branch")
    require(repo["namespace"] in NAMESPACES, f"{name}: invalid namespace")
    require(isinstance(repo["role"], str) and repo["role"], f"{name}: invalid role")
    require(repo["lifecycle"] in LIFECYCLES, f"{name}: invalid lifecycle")
    require(repo["ci_authority"] in CI_AUTHORITIES, f"{name}: invalid ci_authority")
    require(isinstance(repo["local_first"], bool), f"{name}: local_first must be boolean")
    require(
        isinstance(repo["local_artifacts_allowed"], bool),
        f"{name}: local_artifacts_allowed must be boolean",
    )
    require(repo["secret_policy"] == "no-secrets-in-repository", f"{name}: secret policy drift")
    require(repo["quota_criticality"] in QUOTA_LEVELS, f"{name}: invalid quota_criticality")
    require(repo["evidence_status"] in EVIDENCE, f"{name}: invalid evidence_status")

    flags = repo.get("normalization_flags", [])
    require(isinstance(flags, list) and all(isinstance(item, str) for item in flags), f"{name}: invalid normalization_flags")
    secondary = repo.get("ci_secondary", [])
    require(isinstance(secondary, list) and all(isinstance(item, str) for item in secondary), f"{name}: invalid ci_secondary")

    if repo["visibility"] == "public":
        require(
            not repo["local_artifacts_allowed"],
            f"{name}: public repositories cannot allow local artifacts",
        )

    if repo["lifecycle"] == "empty":
        require(repo["size_kb"] == 0, f"{name}: empty lifecycle requires size_kb=0")
        require(repo["ci_authority"] == "none", f"{name}: empty lifecycle requires ci_authority=none")


def main() -> int:
    data = json.loads(MANIFEST.read_text(encoding="utf-8"))

    require(data.get("schema_version") == "1.0.0", "schema_version must be 1.0.0")
    require(data.get("org") == "Copilot-home", "org must be Copilot-home")
    require(
        data.get("source_of_truth") == "github:Copilot-home/DAIOF-Framework",
        "source_of_truth drift",
    )

    repos = data.get("repositories")
    require(isinstance(repos, list) and repos, "repositories must be a non-empty list")

    names: set[str] = set()
    for index, repo in enumerate(repos):
        require(isinstance(repo, dict), f"repositories[{index}] must be an object")
        validate_repo(repo, index)
        name = repo["name"]
        require(name not in names, f"duplicate repository name: {name}")
        names.add(name)

    require(len(repos) == 18, f"expected 18 repositories, found {len(repos)}")

    print(
        json.dumps(
            {
                "status": "PASS",
                "org": data["org"],
                "repository_count": len(repos),
                "source_of_truth": data["source_of_truth"],
            },
            ensure_ascii=False,
        )
    )
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (OSError, json.JSONDecodeError, ValueError) as exc:
        print(json.dumps({"status": "FAIL", "error": str(exc)}, ensure_ascii=False), file=sys.stderr)
        raise SystemExit(1)
