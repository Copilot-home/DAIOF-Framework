# Runtime State Machine

## Objective

Standardize autonomous agent execution inside DAIOF.

The runtime must move through explicit states instead of ad hoc behavior.

---

## Core Runtime States

| State | Meaning |
|---|---|
| IDLE | Waiting for intent |
| CLASSIFYING | Intent classification |
| DECONSTRUCTING | D&R decomposition |
| FOCAL_POINT_ANALYSIS | Identify system focal point |
| SOCRATIC_REFLECTION | Contradiction and risk reflection |
| RISK_ASSIGNMENT | Assign R0-R4 |
| APPROVAL_CHECK | Determine whether approval is required |
| ROUTING | Select smallest safe agent set |
| EXECUTION | Perform action |
| VERIFICATION | Validate result |
| AUDIT | Emit audit event |
| MEMORY_UPDATE | Update durable operational memory |
| ROLLBACK | Restore previous state after failure |
| BLOCKED | Halt due to safety, auth, or policy constraints |
| COMPLETE | Execution completed successfully |

---

## State Transitions

```text
IDLE
→ CLASSIFYING
→ DECONSTRUCTING
→ FOCAL_POINT_ANALYSIS
→ SOCRATIC_REFLECTION
→ RISK_ASSIGNMENT
→ APPROVAL_CHECK
→ ROUTING
→ EXECUTION
→ VERIFICATION
→ AUDIT
→ MEMORY_UPDATE
→ COMPLETE
```

Failure path:

```text
EXECUTION
→ VERIFICATION_FAILED
→ ROLLBACK
→ AUDIT
→ BLOCKED or IDLE
```

---

## Blocking Conditions

The runtime must enter BLOCKED state if:

- authentication expired;
- rollback path unavailable;
- R4 action lacks approval;
- verification fails repeatedly;
- doctrine conflict unresolved;
- connector health unknown for high-risk operation.

---

## Recovery Logic

| Failure | Recovery |
|---|---|
| expired auth | reconnect connector |
| upstream error | retry later or alternate route |
| policy block | reduce scope or request approval |
| verification mismatch | rollback and re-evaluate |
| missing doctrine | halt and escalate |

---

## Governance Constraint

No state transition may bypass:

- risk assignment
- approval checks
- verification
- audit emission

---

## Runtime Goal

The runtime exists to create:

- durable execution
- reversible autonomy
- observable reasoning
- governed orchestration

instead of probabilistic uncontrolled automation.
