# Sovereign Agentic Runtime Doctrine (Canonical)

## Canonical Declaration

DAIOF-Framework is the canonical source-of-truth for the Sovereign Agentic Runtime doctrine, connector lifecycle, runtime state machine, and execution evidence.

## Doctrine Identity

- **Doctrine name**: Sovereign Agentic Runtime
- **Platform scope**: Platform-grade runtime capability for inspectable, auditable, and recoverable agentic execution.
- **Sovereign owner**: Architect Nguyễn Đức Cường (`alpha_prime_omega`)
- **Open-source implementation boundary**:
  - Included: public runtime logic, state specifications, metadata contracts, and evidence mirrors in this repository.
  - Excluded: private credentials, private tool workspaces, and non-public operational data that cannot be safely published.

## Source-of-Truth Metadata Contract

Every runtime/connector registry entry MUST include the following metadata fields:

| Field | Type | Requirement | Description |
| --- | --- | --- | --- |
| `doctrine_version` | string | required | Version of this doctrine being applied. |
| `source_of_truth` | string | required | Canonical system of record (must be `github:NguyenCuong1989/DAIOF-Framework`). |
| `last_synced_from` | string | required | External plane/source of latest mirrored data (for example `asana`, `figma`). |
| `last_verified_at` | string (ISO-8601 UTC) | required | Last verification timestamp in repository. |
| `runtime_consumer` | string | required | Runtime component, team, or process consuming the connector/runtime state. |
| `connector_state` | enum | required | Lifecycle state from connector lifecycle registry. |

## Safety Principles (Non-Negotiable)

- **An toàn**
- **Đường dài**
- **Tin vào số liệu**
- **Hạn chế rủi ro từ con người và AI khi thực thi thủ công**

