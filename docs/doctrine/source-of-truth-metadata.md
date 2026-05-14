---
layout: default
title: Source-of-Truth Metadata Spec
doctrine_version: 0.1.0
source_of_truth: github_repo
last_synced_from: null
last_verified_at: 2026-05-14T23:47:26Z
runtime_consumer: DAIOF-Framework
connector_state: null
---

# Source-of-Truth Metadata (Canonical Fields)

To keep the runtime **inspectable, auditable, and recoverable**, every doctrine page, connector entry, and evidence artifact should carry the following canonical metadata fields.

## Required fields

- `doctrine_version`  
  The doctrine version that governed the artifact when it was written/verified.

- `source_of_truth`  
  Where the canonical truth lives **for this artifact** (typically `github_repo`).

- `last_synced_from`  
  If mirrored from another plane (Asana/Figma/etc), the external reference (URL or identifier). `null` if native to this repo.

- `last_verified_at`  
  Last time the artifact was checked for accuracy (UTC timestamp).

- `runtime_consumer`  
  The runtime(s) that consume the artifact (e.g. `DAIOF-Framework`, `Sovereign Agentic Runtime`).

- `connector_state`  
  Connector lifecycle state when the artifact was verified. For non-connector artifacts, use `null`.

## Applicability rules

- Doctrine pages: include all fields; set `connector_state: null`.
- Connector registry entries: include all fields; `connector_state` must be one of the canonical connector states.
- Evidence artifacts: include all fields; `connector_state` reflects the connector used to produce the evidence (when applicable).

## Example (connector entry)

```yaml
name: Linear
connector_state: DEGRADED
source_of_truth: github_repo
last_synced_from: https://linear.app/
last_verified_at: 2026-05-14T00:00:00Z
runtime_consumer: DAIOF-Framework
doctrine_version: 0.1.0
```

