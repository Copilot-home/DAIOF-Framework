---
layout: default
title: Connector Lifecycle (Canonical)
doctrine_version: 0.1.0
source_of_truth: github_repo
last_synced_from: null
last_verified_at: 2026-05-14T23:47:26Z
runtime_consumer: DAIOF-Framework
connector_state: null
---

# Connector Lifecycle (Canonical)

Connectors are explicit operational dependencies (e.g. GitHub, Figma, Asana). Their lifecycle is modeled as a **finite set of canonical states** with probe-driven transitions and evidence requirements.

Canonical connector states:
- `DISCOVERED`
- `AUTHORIZED`
- `ACTIVE`
- `DEGRADED`
- `EXPIRED`
- `BLOCKED`
- `RETIRED`

## State definitions

- **DISCOVERED**: Connector is known and registered, but not yet validated for use.
- **AUTHORIZED**: Credentials/permissions exist and were validated at least once, but not currently in live use.
- **ACTIVE**: Read/write operations succeed within defined scope, and audit events are emitted.
- **DEGRADED**: Connector is reachable but partially failing (rate limits, intermittent errors, partial scope, partial endpoints).
- **EXPIRED**: Connector authorization is invalid (e.g. 401 session expired, revoked token, expired OAuth grant).
- **BLOCKED**: Runtime policy blocks use (security, safety, or governance reasons), regardless of technical availability.
- **RETIRED**: Connector is intentionally removed from use; kept only for historical evidence and traceability.

## Canonical probes (required)

Each connector must support the probes defined in `docs/runtime/state-machine.md`:
- identity probe
- read probe
- write probe
- permission scope probe
- failure mode classification
- recovery action
- audit event emission

## Transition rules (minimal canonical)

- `DISCOVERED → AUTHORIZED` when **identity + permission scope probes** succeed.
- `AUTHORIZED → ACTIVE` when **read + write probes** succeed and audit events can be recorded.
- `ACTIVE → DEGRADED` when probes fail intermittently or partially, but connector is still reachable.
- `ACTIVE → EXPIRED` when authorization becomes invalid (e.g. 401/403 for previously valid scope).
- `DEGRADED → ACTIVE` when recovery action restores successful probes.
- `DEGRADED → EXPIRED` when failures become authorization-invalid rather than partial degradation.
- `* → BLOCKED` when policy denies use (safety/governance).
- `BLOCKED → (prior state)` only via explicit unblocking decision + verification.
- `* → RETIRED` by explicit retirement decision; no automatic retirement.

## Evidence requirements

Every transition that changes `connector_state` must produce:
- an audit event entry (see `docs/runtime/state-machine.md`)
- an update to `docs/registry/connectors.yml`
- if the transition was caused by an external tool drift (Asana/Figma/etc), an evidence artifact under `docs/evidence/`

