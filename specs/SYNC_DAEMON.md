# Sync Daemon Specification

## Purpose

Define the daemon that keeps DAIOF doctrine, planning state, and runtime registry synchronized across:

- Git repository doctrine
- Linear planning/approval layer
- runtime connector health registry
- audit event stream

The Sync Daemon is not a chatbot. It is an autonomous infrastructure agent governed by doctrine.

---

## Source-of-Truth Hierarchy

1. **Git repository:** canonical doctrine, policies, role contracts, prompts, specs.
2. **Linear:** planning, approval records, issue status, rollout coordination.
3. **Runtime registry:** observed connector state and routing data.
4. **Chat/session memory:** temporary context only.

When sources conflict, repository doctrine wins unless a newer approved doctrine change has been merged through governance workflow.

---

## Core Responsibilities

The Sync Daemon must:

- probe connector health states;
- detect EXPIRED, DEGRADED, BLOCKED, and UPSTREAM_ERROR states;
- compare repo doctrine with Linear planning documents when available;
- update runtime registry from verified observations;
- create audit events for every sync action;
- prevent doctrine drift;
- escalate high-risk or ambiguous changes;
- never store or expose secrets;
- never perform R4 operations automatically.

---

## Non-Goals

The Sync Daemon must not:

- bypass OAuth or user reauthorization;
- paste or store raw tokens;
- auto-merge doctrine changes into main;
- send invoices, deploy production, publish sites, place phone calls, or merge PRs;
- treat Linear as canonical doctrine source;
- overwrite repository doctrine from unverified runtime state.

---

## Runtime State Loop

```text
BOOT
→ LOAD_CANONICAL_DOCTRINE
→ LOAD_RUNTIME_REGISTRY
→ PROBE_CONNECTORS
→ CLASSIFY_HEALTH
→ DETECT_DRIFT
→ PLAN_SYNC_ACTIONS
→ RISK_CLASSIFY_ACTIONS
→ EXECUTE_SAFE_ACTIONS
→ VERIFY_CHANGES
→ EMIT_AUDIT_EVENTS
→ UPDATE_RUNTIME_STATE
→ SLEEP_OR_EXIT
```

Failure path:

```text
PROBE_CONNECTORS
→ AUTH_EXPIRED
→ MARK_EXPIRED
→ BLOCK_R2_R4_FOR_CONNECTOR
→ EMIT_AUDIT_EVENT
→ ESCALATE_REAUTH_REQUIRED
```

---

## Health Classification Rules

| Observation | Health State | Action |
|---|---|---|
| successful profile/list probe | ACTIVE | allow routing within risk policy |
| successful probe with no usable data | ACTIVE_EMPTY | do not use as source-of-truth |
| 401/session expired | EXPIRED | block R2-R4 and request reconnect |
| 403/permission denied | BLOCKED | reduce scope or escalate permission issue |
| 404 object missing | DEGRADED | verify identifiers and use fallback |
| 429/rate limited | DEGRADED | backoff and retry |
| 5xx/upstream failure | UPSTREAM_ERROR | alternate route or retry later |
| registry entry with no probe | DISCOVERED | read-only probe before use |

---

## Drift Detection

The daemon checks drift across three dimensions:

### 1. Doctrine Drift

Repo doctrine differs from Linear doctrine or planning notes.

Response:

- repo remains canonical;
- create/update planning issue if Linear is available;
- open branch/PR if doctrine update is needed;
- audit the drift event.

### 2. Registry Drift

Runtime connector state differs from `CONNECTOR_HEALTH_REGISTRY.json`.

Response:

- update registry only from verified probe evidence;
- commit to governance branch;
- audit state transition.

### 3. Execution Drift

Agent behavior deviates from doctrine.

Response:

- mark violation;
- stop unsafe action;
- create corrective checklist or role prompt update;
- audit and escalate.

---

## Safe Automation Matrix

| Action | Auto? | Risk | Notes |
|---|---:|---:|---|
| read repo doctrine | yes | R1 | canonical source read |
| probe connector identity | yes | R1 | minimal scope |
| mark connector expired | yes | R2 | registry update only |
| update registry on branch | yes | R3 | branch-first controlled write |
| create Linear issue/comment | conditional | R3 | only after Linear active and doctrine-scoped |
| create PR draft | conditional | R3 | allowed when branch state is verified |
| merge PR | no | R4 | explicit approval required |
| deploy production | no | R4 | explicit approval required |
| refresh OAuth token manually | no | R4/secret | never handle raw secrets in chat/logs |

---

## Reauth Handling

When a connector is EXPIRED:

1. Mark connector as EXPIRED in runtime registry.
2. Disable R2-R4 routing for that connector.
3. Use fallback connector if safe.
4. Emit audit event with non-secret metadata.
5. Request human reauthorization through official OAuth UI.
6. After reconnect, run profile probe and minimal list probe.
7. Update `last_verified_at`, `last_synced_from`, and `verification_status`.

---

## Cross-Agent Transaction Policy

For multi-connector operations, the daemon must use a transaction envelope:

```yaml
transaction:
  id: tx_<timestamp>_<short_hash>
  objective: string
  participants:
    - agent: GitHubAgent
      planned_action: create_branch_or_file
      risk: R3
    - agent: LinearAgent
      planned_action: create_issue_or_comment
      risk: R3
  preconditions:
    - all_agents_active
    - rollback_paths_defined
    - approval_state_valid
  commit_order:
    - lowest_external_impact_first
    - canonical_repo_update_before_planning_layer_sync
  rollback:
    - revert_git_commit_or_close_pr
    - close_or_comment_linear_issue
  audit_required: true
```

No cross-agent transaction may include R4 side effects without explicit approval per action.

---

## Audit Requirements

Every daemon cycle that changes state must record:

- timestamp
- daemon version
- source-of-truth version
- connector probed
- previous health state
- new health state
- evidence
- action taken
- risk class
- rollback path
- verification result

---

## Minimal Implementation Sketch

```python
while True:
    doctrine = load_repo_doctrine()
    registry = load_registry()

    for connector in registry.connectors:
        result = probe_minimal_health(connector)
        state = classify_health(result)
        if state != connector.health:
            update_registry(connector, state, evidence=result.summary)
            emit_audit_event(connector, state, result)

    drift = detect_doctrine_drift(repo=doctrine, planning_layer="Linear")
    if drift and linear_is_active():
        create_or_update_planning_issue(drift)

    sleep(schedule_interval)
```

This sketch is conceptual. Real implementation must avoid logging secrets and must run only in an approved runtime environment.

---

## Completion Criteria

Sync Daemon v0.1 is acceptable when it can:

- load repo doctrine;
- load machine-readable registry;
- classify at least ACTIVE, EXPIRED, BLOCKED, and UPSTREAM_ERROR;
- update registry on a branch;
- emit audit events;
- refuse R4 automation;
- report drift between repo and planning layer.

---

## Immediate Runtime Constraint

Linear is currently observed as EXPIRED via `401 Session expired`.

Until reauthorized:

- do not depend on Linear as live planning source;
- keep syncing doctrine to repository;
- mark LinearAgent as expired in runtime registry;
- prepare reauth checklist and post-reauth verification steps.
