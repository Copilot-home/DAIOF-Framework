#!/usr/bin/env python3
from __future__ import annotations

import glob
import re
import sys
import yaml

REQUIRED_TOP_LEVEL = {
    "id",
    "type",
    "version",
    "capabilities",
    "mailbox_in",
    "mailbox_out",
    "scheduler",
    "triggers",
    "state",
    "health",
    "policies",
    "guardrails",
    "contracts",
}
REQUIRED_CONTRACT_KEYS = {"input_schema", "output_schema", "error_schema"}
QUEUE_PATTERN = re.compile(r"^queue\.[a-z0-9_]+\.(in|out)$")

CORE_PROFILES = {
    "conductor": ("search_space_collapse_v1", "deny_rule_update_v1"),
    "mcp_hub": ("dead_end_claim_filter_v1", "claim_rejection_reason_v1"),
    "runtime_observer": ("denied_path_violation_event_v1", "collapse_telemetry_snapshot_v1"),
}


def fail(msg: str) -> None:
    print(f"[FAIL] {msg}")


def main() -> int:
    ok = True
    files = sorted(glob.glob("connectors/*.yaml"))
    if not files:
        fail("No connector files found in connectors/*.yaml")
        return 1

    for path in files:
        with open(path, "r", encoding="utf-8") as f:
            data = yaml.safe_load(f)

        missing = REQUIRED_TOP_LEVEL - set(data.keys())
        if missing:
            ok = False
            fail(f"{path}: missing top-level keys {sorted(missing)}")

        cid = data.get("id")
        if not isinstance(cid, str) or not re.match(r"^[a-z0-9_]+$", cid):
            ok = False
            fail(f"{path}: id must be snake_case string")

        for field in ("mailbox_in", "mailbox_out"):
            val = data.get(field)
            if not isinstance(val, str) or not QUEUE_PATTERN.match(val):
                ok = False
                fail(f"{path}: {field} must match queue.<name>.in|out")

        contracts = data.get("contracts", {})
        missing_contract = REQUIRED_CONTRACT_KEYS - set(contracts.keys()) if isinstance(contracts, dict) else REQUIRED_CONTRACT_KEYS
        if missing_contract:
            ok = False
            fail(f"{path}: contracts missing keys {sorted(missing_contract)}")

        if cid in CORE_PROFILES:
            expected_in, expected_out = CORE_PROFILES[cid]
            in_prof = ((contracts.get("input_schema") or {}).get("profile") if isinstance(contracts, dict) else None)
            out_prof = ((contracts.get("output_schema") or {}).get("profile") if isinstance(contracts, dict) else None)
            if in_prof != expected_in:
                ok = False
                fail(f"{path}: input_schema.profile expected {expected_in}, got {in_prof}")
            if out_prof != expected_out:
                ok = False
                fail(f"{path}: output_schema.profile expected {expected_out}, got {out_prof}")

    if ok:
        print(f"[PASS] Connector standardization validated for {len(files)} files")
        return 0
    return 1


if __name__ == "__main__":
    sys.exit(main())
