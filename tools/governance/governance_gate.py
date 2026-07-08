#!/usr/bin/env python3
"""Generate and validate DAIOF governance and runtime-topology evidence."""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
import re
import sys
from pathlib import Path
from typing import Any

import yaml

SCHEMA_VERSION = "1.0.0"
DEFAULT_MANIFEST = Path("governance/workflow_manifest.json")
DEFAULT_RUNTIME_TOPOLOGY = Path("governance/runtime_topology.json")
DEFAULT_CHOICE_REVIEW = Path("governance/choice_review.json")
DEFAULT_DR_REVIEW = Path("governance/dr_review.json")
DEFAULT_RUNTIME_ADAPTERS = Path("governance/runtime_adapters.json")
DEFAULT_RUNTIME_ATTESTATION_SCHEMA = Path("governance/runtime_attestation.schema.json")
DEPLOY_TERMS = ("deploy", "publish", "release", "pypi", "docker")
FULL_SHA = re.compile(r"^[0-9a-fA-F]{40}$")


class WorkflowLoader(yaml.SafeLoader):
    """YAML loader that keeps the key ``on`` as a string under YAML 1.1."""


WorkflowLoader.yaml_implicit_resolvers = copy.deepcopy(
    yaml.SafeLoader.yaml_implicit_resolvers
)
for first_char, resolvers in list(WorkflowLoader.yaml_implicit_resolvers.items()):
    WorkflowLoader.yaml_implicit_resolvers[first_char] = [
        resolver for resolver in resolvers if resolver[0] != "tag:yaml.org,2002:bool"
    ]


def load_json(path: Path) -> dict[str, Any]:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise ValueError(f"missing required artifact: {path}") from exc
    except json.JSONDecodeError as exc:
        raise ValueError(f"invalid JSON in {path}: {exc}") from exc


def dump_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )


def sha256(path: Path) -> str:
    # GitHub runners and Windows worktrees can materialize YAML with different
    # line endings. Governance hashes must describe content, not checkout OS.
    normalized = path.read_text(encoding="utf-8").replace("\r\n", "\n")
    return hashlib.sha256(normalized.encode("utf-8")).hexdigest()


def normalize_list(value: Any) -> list[str]:
    if value is None:
        return []
    if isinstance(value, list):
        return [str(item) for item in value]
    return [str(value)]


def action_reference(step: Any) -> str | None:
    if not isinstance(step, dict):
        return None
    uses = step.get("uses")
    return str(uses) if uses else None


def is_pinned_action(reference: str) -> bool:
    if reference.startswith("./") or reference.startswith("docker://"):
        return True
    if "@" not in reference:
        return False
    return bool(FULL_SHA.fullmatch(reference.rsplit("@", 1)[1]))


def workflow_record(path: Path, root: Path) -> dict[str, Any]:
    try:
        data = yaml.load(path.read_text(encoding="utf-8"), Loader=WorkflowLoader) or {}
    except yaml.YAMLError as exc:
        raise ValueError(f"invalid workflow YAML in {path}: {exc}") from exc

    jobs = data.get("jobs") or {}
    if not isinstance(jobs, dict):
        raise ValueError(f"workflow jobs must be a mapping: {path}")

    action_refs: list[str] = []
    job_records: list[dict[str, Any]] = []
    for job_id, raw_job in sorted(jobs.items()):
        job = raw_job if isinstance(raw_job, dict) else {}
        refs = [
            ref
            for ref in (action_reference(step) for step in job.get("steps", []))
            if ref is not None
        ]
        action_refs.extend(refs)
        job_records.append(
            {
                "id": str(job_id),
                "needs": sorted(normalize_list(job.get("needs"))),
                "permissions": job.get("permissions"),
                "environment": job.get("environment"),
                "actions": sorted(refs),
            }
        )

    trigger_data = data.get("on") or {}
    if isinstance(trigger_data, dict):
        triggers = sorted(str(key) for key in trigger_data)
    else:
        triggers = sorted(normalize_list(trigger_data))

    relative = path.relative_to(root).as_posix()
    search_text = f"{path.name} {data.get('name', '')} {' '.join(str(key) for key in jobs)}".lower()
    deploy_capable = any(term in search_text for term in DEPLOY_TERMS)
    explicit_permissions = data.get("permissions") is not None or all(
        record["permissions"] is not None for record in job_records
    )
    pinned_count = sum(is_pinned_action(ref) for ref in action_refs)

    return {
        "path": relative,
        "name": str(data.get("name") or path.stem),
        "sha256": sha256(path),
        "triggers": triggers,
        "permissions": data.get("permissions"),
        "jobs": job_records,
        "deploy_capable": deploy_capable,
        "explicit_permissions": explicit_permissions,
        "action_references": len(action_refs),
        "pinned_action_references": pinned_count,
        "unpinned_actions": sorted(
            ref for ref in action_refs if not is_pinned_action(ref)
        ),
    }


def build_manifest(root: Path) -> dict[str, Any]:
    workflow_dir = root / ".github" / "workflows"
    paths = sorted([*workflow_dir.glob("*.yml"), *workflow_dir.glob("*.yaml")])
    workflows = [workflow_record(path, root) for path in paths]
    total_actions = sum(item["action_references"] for item in workflows)
    pinned_actions = sum(item["pinned_action_references"] for item in workflows)
    explicit = sum(item["explicit_permissions"] for item in workflows)
    deploy_workflows = [item["path"] for item in workflows if item["deploy_capable"]]

    return {
        "schema_version": SCHEMA_VERSION,
        "source": ".github/workflows",
        "workflow_count": len(workflows),
        "metrics": {
            "explicit_permission_coverage": (
                round(explicit / len(workflows), 4) if workflows else 1.0
            ),
            "pinned_action_rate": (
                round(pinned_actions / total_actions, 4) if total_actions else 1.0
            ),
            "deploy_workflow_count": len(deploy_workflows),
            "workflow_drift_rate": 0.0,
        },
        "deploy_workflows": deploy_workflows,
        "workflows": workflows,
    }


def validate_choice_review(review: dict[str, Any], errors: list[str]) -> None:
    required = {
        "intent_validation",
        "risk_forecast",
        "deployment_justification",
        "override_tracking",
        "human_approval",
    }
    missing = sorted(required - review.keys())
    if missing:
        errors.append(f"choice_review missing fields: {', '.join(missing)}")
    if review.get("schema_version") != SCHEMA_VERSION:
        errors.append("choice_review schema_version mismatch")
    if not review.get("risk_forecast"):
        errors.append("choice_review risk_forecast must not be empty")
    approval = review.get("human_approval") or {}
    if approval.get("required") is not True:
        errors.append("choice_review must require human approval")


def validate_dr_review(review: dict[str, Any], errors: list[str]) -> None:
    required = {
        "deconstruction",
        "focal_point",
        "rearchitecture",
        "pillars",
        "risk_graph",
    }
    missing = sorted(required - review.keys())
    if missing:
        errors.append(f"dr_review missing fields: {', '.join(missing)}")
    if review.get("schema_version") != SCHEMA_VERSION:
        errors.append("dr_review schema_version mismatch")
    pillars = review.get("pillars") or {}
    for pillar in ("safety", "longevity", "data_driven", "human_ai_risk_control"):
        score = pillars.get(pillar)
        if not isinstance(score, (int, float)) or score < 7.0:
            errors.append(f"dr_review pillar {pillar} must be >= 7.0")


def validate_runtime_topology(
    topology: dict[str, Any], manifest: dict[str, Any], errors: list[str]
) -> None:
    if topology.get("schema_version") != SCHEMA_VERSION:
        errors.append("runtime_topology schema_version mismatch")
    components = topology.get("components") or []
    component_ids = {item.get("id") for item in components if isinstance(item, dict)}
    required_components = {
        "github_actions",
        "openclaw_gateway",
        "planner_service",
        "phoenix_council",
        "factory_executor",
        "axcontrol",
        "ril",
        "hypercore",
        "the_choice",
        "dr_protocol",
        "artifact_chain",
        "deployment_runtime",
    }
    missing = sorted(required_components - component_ids)
    if missing:
        errors.append(f"runtime_topology missing components: {', '.join(missing)}")

    paths = topology.get("deployment_paths") or []
    mapped_workflows = {
        path.get("workflow") for path in paths if isinstance(path, dict)
    }
    for workflow in manifest.get("deploy_workflows", []):
        if workflow not in mapped_workflows:
            errors.append(
                f"deploy workflow is not mapped to runtime topology: {workflow}"
            )
    for path in paths:
        if not path.get("required_components"):
            errors.append(
                f"deployment path has no required components: {path.get('workflow')}"
            )
        if path.get("missing_evidence_policy") != "block":
            errors.append(
                f"deployment path must block on missing evidence: {path.get('workflow')}"
            )


def validate_runtime_adapters(
    adapters: dict[str, Any], topology: dict[str, Any], errors: list[str]
) -> None:
    if adapters.get("schema_version") != SCHEMA_VERSION:
        errors.append("runtime_adapters schema_version mismatch")
    if (
        not isinstance(adapters.get("ttl_seconds"), int)
        or adapters.get("ttl_seconds", 0) <= 0
    ):
        errors.append("runtime_adapters ttl_seconds must be a positive integer")
    for field in ("attestation_hmac_key_env", "attestation_key_id_env"):
        if not adapters.get(field):
            errors.append(f"runtime_adapters missing signing field: {field}")
    supported_types = {"http_json", "file_json"}
    configured: set[str] = set()
    for component in adapters.get("components", []):
        if not isinstance(component, dict) or not component.get("id"):
            errors.append("runtime_adapters contains an invalid component")
            continue
        component_id = str(component["id"])
        if component_id in configured:
            errors.append(
                f"runtime_adapters contains duplicate component: {component_id}"
            )
        configured.add(component_id)
        adapter = component.get("adapter") or {}
        if adapter.get("type") not in supported_types:
            errors.append(f"runtime adapter type is unsupported for {component_id}")
        for field in (
            "identity_path",
            "expected_identity",
            "version_path",
            "health_path",
        ):
            if not adapter.get(field):
                errors.append(f"runtime adapter {component_id} missing field: {field}")
        if not adapter.get("healthy_values"):
            errors.append(f"runtime adapter {component_id} has no healthy_values")
        if adapter.get("type") == "http_json" and not adapter.get("url_env"):
            errors.append(f"HTTP runtime adapter {component_id} must use url_env")
        if adapter.get("type") == "file_json" and not adapter.get("path_env"):
            errors.append(f"file runtime adapter {component_id} must use path_env")
        if any(key in adapter for key in ("url", "token", "path")):
            errors.append(
                f"runtime adapter {component_id} must not embed endpoint paths or secrets"
            )

    external = {
        str(component.get("id"))
        for component in topology.get("components", [])
        if isinstance(component, dict)
        and component.get("evidence_state") == "external_evidence_required"
    }
    missing = sorted(external - configured)
    if missing:
        errors.append(
            f"external runtime components lack evidence adapters: {', '.join(missing)}"
        )


def validate_attestation_schema(schema: dict[str, Any], errors: list[str]) -> None:
    required = set(schema.get("required", []))
    expected = {
        "schema_version",
        "attestation_type",
        "environment",
        "generated_at",
        "expires_at",
        "topology_sha256",
        "adapter_config_sha256",
        "components",
        "summary",
        "attestation_sha256",
        "signing",
    }
    missing = sorted(expected - required)
    if missing:
        errors.append(
            f"runtime attestation schema missing required fields: {', '.join(missing)}"
        )


def validate_workflow_safety(
    root: Path, manifest: dict[str, Any], errors: list[str]
) -> None:
    for workflow in manifest.get("workflows", []):
        path = root / workflow["path"]
        content = path.read_text(encoding="utf-8")
        merge_patterns = (
            "github.rest.pulls.merge",
            "gh pr merge",
            "mergePullRequest",
        )
        if any(pattern in content for pattern in merge_patterns):
            errors.append(f"direct merge API bypass is forbidden: {workflow['path']}")
        if "event: 'APPROVE'" in content or 'event: "APPROVE"' in content:
            errors.append(
                f"workflow-generated PR approval is forbidden: {workflow['path']}"
            )


def validate(root: Path, write_manifest: bool = False) -> list[str]:
    errors: list[str] = []
    generated = build_manifest(root)
    manifest_path = root / DEFAULT_MANIFEST
    if write_manifest:
        dump_json(manifest_path, generated)
    else:
        try:
            committed = load_json(manifest_path)
            if committed != generated:
                errors.append(
                    "workflow_manifest.json drift detected; run governance_gate.py generate"
                )
        except ValueError as exc:
            errors.append(str(exc))

    runtime: dict[str, Any] | None = None
    try:
        runtime = load_json(root / DEFAULT_RUNTIME_TOPOLOGY)
        validate_runtime_topology(runtime, generated, errors)
    except ValueError as exc:
        errors.append(str(exc))
    if runtime is not None:
        try:
            adapters = load_json(root / DEFAULT_RUNTIME_ADAPTERS)
            validate_runtime_adapters(adapters, runtime, errors)
        except ValueError as exc:
            errors.append(str(exc))
    try:
        schema = load_json(root / DEFAULT_RUNTIME_ATTESTATION_SCHEMA)
        validate_attestation_schema(schema, errors)
    except ValueError as exc:
        errors.append(str(exc))
    try:
        validate_choice_review(load_json(root / DEFAULT_CHOICE_REVIEW), errors)
    except ValueError as exc:
        errors.append(str(exc))
    try:
        validate_dr_review(load_json(root / DEFAULT_DR_REVIEW), errors)
    except ValueError as exc:
        errors.append(str(exc))
    validate_workflow_safety(root, generated, errors)
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command", choices=("generate", "validate", "report"))
    parser.add_argument("--root", type=Path, default=Path.cwd())
    args = parser.parse_args()
    root = args.root.resolve()

    if args.command == "generate":
        errors = validate(root, write_manifest=True)
    elif args.command == "report":
        print(json.dumps(build_manifest(root), indent=2, sort_keys=True))
        return 0
    else:
        errors = validate(root)

    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        return 1
    print("Governance gate passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
