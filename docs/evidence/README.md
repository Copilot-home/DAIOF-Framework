---
layout: default
title: Execution Evidence (Canonical)
doctrine_version: 0.1.0
source_of_truth: github_repo
last_synced_from: null
last_verified_at: 2026-05-14T23:47:26Z
runtime_consumer: DAIOF-Framework
connector_state: null
---

# Execution Evidence (Canonical)

Goal: keep GitHub (this repo) canonical even if external operational tools drift, expire, or become inaccessible.

External planes (examples):
- Asana: execution backlog substrate
- Figma: visual topology substrate
- Linear: degraded/expired sessions possible
- Airtable: requires verification before operational reliance

## Evidence invariants

- Evidence must be **human-reviewable** and **repo-storable**.
- Every evidence artifact must include the canonical metadata fields defined in `docs/doctrine/source-of-truth-metadata.md`.
- Any connector-driven decision (state changes, governance changes) must be reflected in:
  - `docs/registry/connectors.yml` (connector state)
  - `docs/registry/evidence-registry.yml` (evidence pointer)

## How to mirror evidence from external tools

1) Create a new evidence file under `docs/evidence/` using a template:
- External artifact template: `docs/evidence/templates/external-artifact.md`
- Decision record template: `docs/evidence/templates/decision-record.md`

2) Add an entry to `docs/registry/evidence-registry.yml` that points to the new evidence file.

3) Ensure `last_synced_from` contains the external URL/id (no secrets), and `last_verified_at` is updated.

## What counts as “critical evidence”

- Decisions that change connector lifecycle state
- Runtime permission scope decisions (least privilege changes)
- Operational topology snapshots (Figma frames exported, high-level diagrams)
- Backlog commitments and outcomes (Asana milestones mirrored into GitHub issues/docs)

