---
layout: default
title: Canonical Registries
doctrine_version: 0.1.0
source_of_truth: github_repo
last_synced_from: null
last_verified_at: 2026-05-14T23:47:26Z
runtime_consumer: DAIOF-Framework
connector_state: null
---

# Canonical Registries

Registries are machine-readable inventories that make the runtime **inspectable** and **auditable**.

## Connector registry

- File: `docs/registry/connectors.yml`
- Purpose: single place to view connector inventory, ownership, state, and verification timestamps.
- Lifecycle semantics: `docs/runtime/connector-lifecycle.md`

## Evidence registry (execution evidence)

- Folder: `docs/evidence/`
- Purpose: mirror critical operational evidence from external planes into the repo so GitHub remains canonical.

## Update rules

- Any connector state change must update `docs/registry/connectors.yml`.
- Any mirrored artifact must record `last_synced_from` and `last_verified_at` per `docs/doctrine/source-of-truth-metadata.md`.

