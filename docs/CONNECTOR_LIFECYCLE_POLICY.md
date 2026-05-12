# Connector Lifecycle Policy

## Purpose

Define how DAIOF handles authenticated connector agents across connection, probing, operation, expiration, recovery, drift prevention, and retirement.

---

## Canonical Source-of-Truth Rule

- **Repository:** canonical doctrine and policy source.
- **Linear:** planning, approval, rollout, and synchronization coordination layer.
- **Runtime registry:** operational state consumed by agents.
- **Chat:** temporary context only.

---

## Connector Lifecycle States

| State | Meaning | Runtime Behavior |
|---|---|---|
| DISCOVERED | Tool surface exists but identity not verified | Only R0/R1 probe allowed |
| ACTIVE | Authenticated and usable | Route normally within risk class |
| ACTIVE_EMPTY | Authenticated but no useful data | Do not use as source-of-truth; seed or bypass |
| DEGRADED | Partial failures or limited tool path | Prefer alternate agent; log limitation |
| EXPIRED | Session/token expired | Block write operations; require reconnect |
| BLOCKED | Safety/policy layer blocked current path | Reduce scope or request explicit approval |
| UPSTREAM_ERROR | External service failed | Retry later or alternate route |
| RETIRED | No longer trusted/used | Remove from routing except audit/history |

---

## Reauthorization Policy

When connector session expires:

1. Mark connector as `EXPIRED` in runtime registry.
2. Stop all R2-R4 operations through that connector.
3. Continue only with documented fallback agents if safe.
4. User/Architect must reauthorize through the platform OAuth flow.
5. After reconnect, run identity probe.
6. Run minimal search/list probe.
7. Update `last_verified_at` and `last_synced_from`.
8. Resume routing only after successful verification.

---

## Linear Reauthorization Procedure

When Linear returns `401 Session expired`:

1. Reconnect the Linear integration through the host application UI.
2. Verify access under Linear authorized applications.
3. Ensure OAuth refresh tokens are enabled when managing a custom Linear OAuth app.
4. Do not paste raw access tokens or refresh tokens into chat, repo, issues, logs, or prompts.
5. After reconnect, run:
   - profile probe
   - workspace/team probe
   - `WWW-113` issue fetch
   - `DAIOF_Codex_AI_Native_Engineering_Doctrine` document fetch
6. Compare Linear doctrine against repo doctrine.
7. Resolve drift by updating the canonical repo doctrine or opening an explicit planning issue.

---

## Drift Prevention

Every doctrine-bearing artifact should include:

- `source_of_truth`
- `doctrine_version`
- `last_synced_from`
- `last_verified_at`
- `verification_status`

If Linear and repo disagree:

1. Repository doctrine remains canonical by default.
2. Linear records the planning/approval delta.
3. Runtime must consume the repo version until a new version is merged.

---

## Token and Secret Policy

Agents must never:

- request raw tokens in chat;
- store access tokens in repo;
- log refresh tokens;
- expose credentials in audit events;
- create screenshots or plaintext copies of OAuth secrets.

Allowed:

- ask user to reconnect through official OAuth UI;
- record connector health state;
- record non-secret account/workspace identifiers when useful for audit.

---

## Recovery Decision Table

| Failure | State | Action |
|---|---|---|
| 401/expired session | EXPIRED | Reconnect OAuth, then identity probe |
| 403/permission denied | BLOCKED | Reduce scope or request permission change |
| 404 object missing | DEGRADED | Verify ID and fallback source |
| 429/rate limit | DEGRADED | Backoff and retry later |
| 5xx/upstream error | UPSTREAM_ERROR | Alternate route or retry later |
| Empty data | ACTIVE_EMPTY | Seed sandbox or bypass |

---

## Operational Invariant

No high-impact action may depend on an expired, unverified, blocked, or stale connector state.

---

## Next Required Action for Linear

Once reauthorized, update:

- `CONNECTOR_HEALTH_REGISTRY.json`
- `CODEX_AI_NATIVE_ENGINEERING_TEAM_MAPPING.md`
- `last_verified_at` fields
- Linear anchor issue `WWW-113`

and record an audit event for the sync.
