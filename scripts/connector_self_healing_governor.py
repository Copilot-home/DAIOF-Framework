#!/usr/bin/env python3
from __future__ import annotations

import json
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
MATRIX = ROOT / "docs/operations/CONNECTOR_HEALTH_MATRIX.yaml"

BLOCK_MUTATION_STATES = {"auth_stale", "broken", "production_guarded", "unknown"}
ADAPTER_STATES = {"ready_with_adapter"}
SAFE_STATES = {"ready", "legacy_ready"}

def load_matrix() -> dict:
    if not MATRIX.exists():
        raise SystemExit(f"missing matrix: {MATRIX}")
    return yaml.safe_load(MATRIX.read_text(encoding="utf-8"))

def classify(connector: str, action: str) -> dict:
    m = load_matrix()
    cfg = m.get("connectors", {}).get(connector)
    if not cfg:
        return {
            "decision": "DENY",
            "reason": "unknown_connector",
            "connector": connector,
            "action": action,
        }

    state = cfg.get("state", "unknown")
    allowed = set(cfg.get("allowed_actions", []))
    blocked = set(cfg.get("blocked_actions", []))

    if action in blocked:
        decision = "DENY"
        reason = "explicitly_blocked_action"
    elif state == "production_guarded" and any(x in action for x in ["create", "refund", "invoice", "payment", "charge", "customer_mutation"]):
        decision = "DENY"
        reason = "financial_mutation_blocked"
    elif state in BLOCK_MUTATION_STATES and action not in allowed:
        decision = "DENY"
        reason = f"state_{state}_requires_guard"
    elif state in ADAPTER_STATES:
        decision = "ALLOW_WITH_ADAPTER"
        reason = "normalizer_required"
    elif state in SAFE_STATES or action in allowed:
        decision = "ALLOW"
        reason = "policy_pass"
    else:
        decision = "REVIEW"
        reason = f"state_{state}_not_fully_classified"

    return {
        "decision": decision,
        "reason": reason,
        "connector": connector,
        "state": state,
        "owner_agent": cfg.get("owner_agent"),
        "action": action,
        "next_action": cfg.get("next_action"),
        "issue_codes": cfg.get("issue_codes", []),
    }

def main() -> int:
    if len(sys.argv) < 3:
        print("usage: connector_self_healing_governor.py <connector> <action>")
        return 2
    print(json.dumps(classify(sys.argv[1], sys.argv[2]), ensure_ascii=False, indent=2))
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
