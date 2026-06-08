# Connector Lifecycle and Runtime State Machine Registry

This document is the operational registry for connector lifecycle state, runtime probe transitions, and mirrored execution evidence.

## Canonical Metadata

- `doctrine_version`: `1.0.0`
- `source_of_truth`: `github:NguyenCuong1989/DAIOF-Framework`
- `last_synced_from`: `asana,figma,linear,airtable`
- `last_verified_at`: `2026-05-14T23:47:14Z`
- `runtime_consumer`: `Sovereign Agentic Runtime`

## Connector Lifecycle States

### State Definitions

- `DISCOVERED`: Connector is identified but not yet authenticated.
- `AUTHORIZED`: Connector authentication is valid; scope handshake completed.
- `ACTIVE`: Connector read/write path healthy and operational.
- `DEGRADED`: Connector reachable but one or more probes failing or unstable.
- `EXPIRED`: Connector authorization/session expired and requires renewal.
- `BLOCKED`: Connector is intentionally or externally blocked from runtime use.
- `RETIRED`: Connector intentionally decommissioned and excluded from runtime graph.

### Registry

| Connector | Connector state | Runtime consumer | Last synced from | Last verified at | Notes |
| --- | --- | --- | --- | --- | --- |
| GitHub | ACTIVE | Sovereign Agentic Runtime | github | 2026-05-14T23:47:14Z | Canonical repository substrate. |
| Figma | ACTIVE | Sovereign Agentic Runtime | figma | 2026-05-14T23:47:14Z | Visual topology substrate. |
| Asana | ACTIVE | Sovereign Agentic Runtime | asana | 2026-05-14T23:47:14Z | Execution backlog substrate. |
| Linear | EXPIRED | Sovereign Agentic Runtime | linear | 2026-05-14T23:47:14Z | Session returned 401; re-authorization required. |
| Airtable | DISCOVERED | Sovereign Agentic Runtime | airtable | 2026-05-14T23:47:14Z | Requires verification re-check. |

## Runtime State Machine Transition Probes

| Transition checkpoint | identity probe | read probe | write probe | permission scope probe | failure mode | recovery action | audit event |
| --- | --- | --- | --- | --- | --- | --- | --- |
| DISCOVERED → AUTHORIZED | Validate connector principal ID/owner | Read connector profile metadata | N/A | Confirm requested scopes | Invalid identity or auth handshake rejected | Re-run auth flow with explicit owner binding | `connector.authorization.attempted` |
| AUTHORIZED → ACTIVE | Re-confirm active token identity | Read lightweight health payload | Write no-op or draft heartbeat | Verify minimum runtime scopes still present | Token revoked, scope drift, write denied | Refresh token/session and re-scope | `connector.activation.probe` |
| ACTIVE → DEGRADED | Identity still resolves | Read latency/error threshold exceeded | Write intermittently fails | Scope partially valid | Partial outage, throttling, elevated error rate | Enter safe-mode retries and reduce write pressure | `connector.degraded.detected` |
| DEGRADED → ACTIVE | Identity stable after mitigation | Read probe success restored | Write probe success restored | Scope check returns full required set | Recovery incomplete | Keep degraded safeguards active until all probes pass | `connector.recovery.completed` |
| ANY → EXPIRED | Identity cannot be validated due to expired session | Read returns auth/session errors | Write denied with auth/session errors | Scope inaccessible | Session/token expiration | Re-authorize and re-run full probe chain | `connector.session.expired` |
| ANY → BLOCKED | Identity may resolve but policy denies use | Read intentionally disabled | Write intentionally disabled | Scope blocked by policy/compliance gate | Governance or security block | Escalate to owner decision and document unblock criteria | `connector.blocked.enforced` |
| ANY → RETIRED | Identity archived for audit only | Read optional for historical export | Write disabled permanently | Scope revoked permanently | Connector sunset | Archive evidence and remove from active runtime graph | `connector.retired.archived` |

## Execution Evidence Mirror (Canonical in GitHub)

Operational evidence from external execution planes MUST be mirrored into repository issues/docs to keep GitHub canonical even when tools drift.

| Plane | Expected mirror artifact in repository | Current status snapshot |
| --- | --- | --- |
| GitHub | Issues, PRs, workflow runs, operations docs | ACTIVE |
| Figma | Issue/docs snapshot links and topology version notes | ACTIVE |
| Asana | Issue/docs snapshot of backlog status and key execution evidence | ACTIVE |
| Linear | Issue/docs incident entry with session status and recovery plan | EXPIRED (401) |
| Airtable | Issue/docs verification checkpoint and decision record | RE-CHECK REQUIRED |
