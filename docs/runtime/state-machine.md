---
layout: default
title: Runtime State Machine + Transition Probes (Canonical)
doctrine_version: 0.1.0
source_of_truth: github_repo
last_synced_from: null
last_verified_at: 2026-05-14T23:47:26Z
runtime_consumer: DAIOF-Framework
connector_state: null
---

# Runtime State Machine + Transition Probes (Canonical)

SAR requires an explicit, probe-driven state machine so the runtime is **inspectable, auditable, and recoverable**.

This document defines the canonical probes and the minimal evidence emitted for connector transitions.

## Scope

- **Connector lifecycle states** are canonicalized in `docs/runtime/connector-lifecycle.md`.
- This document defines **how** the runtime decides transitions (probes) and **what evidence** must be recorded.

## Canonical transition probes

Every connector transition decision must evaluate and record these probes:

1) **Identity probe**
- Verifies the runtime can identify itself and the connector identity it is operating as.
- Evidence: identity claims (non-secret), connector account/tenant identifiers, and runtime consumer identifier.

2) **Read probe**
- Verifies minimum read operation(s) for the connector succeed within expected latency and error budget.
- Evidence: endpoint/action name, result status, latency, and redacted response summary.

3) **Write probe**
- Verifies minimum write operation(s) succeed (or are explicitly disabled by policy).
- Evidence: action name, dry-run vs live, result status, and redacted payload summary.

4) **Permission scope probe**
- Verifies the connector authorization includes required scopes and is not broader than intended.
- Evidence: required scopes, observed scopes (redacted), scope diff decision.

5) **Failure mode**
- Classifies the failure in a stable taxonomy (examples):
  - `AUTH_EXPIRED` (401/expired session)
  - `SCOPE_INSUFFICIENT` (403/insufficient)
  - `RATE_LIMITED`
  - `NETWORK_UNREACHABLE`
  - `PARTIAL_OUTAGE`
  - `POLICY_BLOCKED`

6) **Recovery action**
- Records the canonical next action to restore health (examples):
  - re-authenticate / renew token
  - reduce scope to least privilege
  - backoff + retry strategy
  - switch to degraded read-only mode
  - escalate to human review

7) **Audit event**
- Emits a structured audit event for every transition decision, including “no change”.

## Audit event (minimum schema)

Audit events must be storable as plain text in this repo (or as GitHub issue comments) and reference any evidence artifacts under `docs/evidence/`.

```yaml
timestamp: 2026-05-14T23:47:26Z
runtime_consumer: DAIOF-Framework
connector: Linear
state_from: ACTIVE
state_to: DEGRADED
probe_results:
  identity: pass
  read: pass
  write: fail
  permission_scope: unknown
failure_mode: AUTH_EXPIRED
recovery_action: re-authorize connector session; re-run probes
evidence_refs:
  - docs/evidence/templates/external-artifact.md
```

## Transition decision rules (minimal)

- If **identity** or **permission scope** probes fail due to invalid authorization, transition to `EXPIRED`.
- If **read** or **write** probes partially fail but authorization remains valid, transition to `DEGRADED`.
- If policy prohibits usage, transition to `BLOCKED` regardless of technical status.
- Recovery transitions require explicit evidence of probe success and an audit event.

