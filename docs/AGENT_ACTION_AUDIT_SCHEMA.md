# Agent Action Audit Schema

## Purpose

Standardize all authenticated-agent actions executed inside the DAIOF mesh.

Every action must be reconstructable from logs.

---

## Core Principle

No execution without:

- intent
- selected agent
- evidence
- risk classification
- result
- verification

---

## Canonical Audit Event

```json
{
  "timestamp": "2026-05-12T00:00:00Z",
  "session_id": "optional-chat-session-id",
  "architect": "alpha_prime_omega",
  "orchestrator": "ChatGPT/DAIOF",
  "intent": "Create governance registry for authenticated agent mesh",
  "dr_phase": {
    "deconstruction": "Connector ecosystem mapped",
    "focal_point": "Need machine-readable governance",
    "rearchitecture": "Create registry JSON on governance branch"
  },
  "selected_agent": "GitHubAgent",
  "connector": "GitHub",
  "health_state": "active",
  "risk_class": "R3",
  "target": {
    "repository": "NguyenCuong1989/DAIOF-Framework",
    "branch": "architect/connector-governance-kernel-v0.2",
    "path": "docs/CONNECTOR_HEALTH_REGISTRY.json"
  },
  "evidence": [
    "Repository permissions verified",
    "Branch existence verified"
  ],
  "execution": {
    "action": "create_file",
    "status": "success",
    "commit_sha": "example_sha"
  },
  "verification": {
    "post_write_check": true,
    "main_branch_untouched": true
  },
  "socratic_reflection": {
    "question": "Was this action reversible and governed?",
    "answer": "Yes; isolated on governance branch"
  },
  "next_action": "Create pull request after review"
}
```

---

## Required Fields

| Field | Description |
|---|---|
| timestamp | ISO8601 execution time |
| intent | Human or orchestrator goal |
| selected_agent | Which authenticated agent executed |
| risk_class | R0-R4 classification |
| evidence | Observed facts supporting action |
| execution.status | success / partial_failure / failed |
| verification | Post-execution validation |

---

## Failure Event Example

```json
{
  "selected_agent": "LinearAgent",
  "health_state": "expired",
  "execution": {
    "status": "failed",
    "error_type": "authentication_expired"
  },
  "recovery_path": "Reauthenticate connector"
}
```

---

## Mesh Governance Rules

1. Every R3/R4 action must emit an audit event.
2. Every failed action must include recovery_path.
3. Every external side effect must include explicit confirmation evidence.
4. Branch-first mutations should record branch name.
5. Financial operations must record customer-safe summaries only.
6. Raw secrets/API keys must never enter audit logs.
7. Audit events should remain append-only.

---

## Future Extensions

- Signed audit events
- Cross-agent trace IDs
- Distributed execution graphs
- Replayable orchestration history
- Runtime anomaly detection
- Human approval signatures
- Autonomous rollback policies

---

## Governance Statement

The audit layer exists to ensure that AI autonomy remains:

- observable
- reconstructable
- bounded
- reversible
- aligned with the Four Pillars

without reducing execution capability.
