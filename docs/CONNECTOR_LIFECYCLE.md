# 🔌 Connector Lifecycle Specification

**Version:** 1.0.0
**Status:** CANONICAL SPECIFICATION
**Architect:** Nguyễn Đức Cường (alpha_prime_omega)
**Verification Code:** 4287
**Last Updated:** 2026-05-14

---

## 📋 Overview

This document defines the canonical lifecycle states and transitions for connectors in the Sovereign Agentic Runtime. Connectors are external tool integrations (e.g., Asana, Figma, Linear, Airtable) that serve as operational substrates while GitHub remains the canonical source-of-truth.

---

## 🎯 Connector Philosophy

**Key Principles:**
1. **GitHub is Canonical**: All external tools are substrates, not sources-of-truth
2. **Drift Tolerance**: Repository remains operational even if connectors drift
3. **Evidence Mirroring**: Operational data must be mirrored to repository
4. **State Transparency**: Connector state must be observable and auditable
5. **Graceful Degradation**: System functions even when connectors fail

---

## 📊 Connector States

### State Diagram

```
                    ┌─────────────┐
                    │  DISCOVERED │ ◄─── Initial detection
                    └──────┬──────┘
                           │
                    [Identity Probe]
                           │
                           ▼
                    ┌─────────────┐
            ┌───────┤ AUTHORIZED  │ ◄─── Credentials valid
            │       └──────┬──────┘
            │              │
            │       [Permission Scope Probe]
            │              │
            │              ▼
            │       ┌─────────────┐
            │       │   ACTIVE    │ ◄─── Fully operational
            │       └──────┬──────┘
            │              │
            │       [Read/Write Probes]
            │              │
            │       ┌──────┴──────┬──────────┬──────────┐
            │       ▼             ▼          ▼          ▼
            │  ┌─────────┐  ┌─────────┐ ┌────────┐ ┌────────┐
            │  │DEGRADED │  │ EXPIRED │ │BLOCKED │ │RETIRED │
            │  └────┬────┘  └────┬────┘ └───┬────┘ └───┬────┘
            │       │            │          │          │
            │  [Recovery]   [Re-auth]  [Unblock]  [Decommission]
            │       │            │          │          │
            └───────┴────────────┴──────────┴──────────┘
                                  │
                                  ▼
                            [Final State]
```

---

## 🏷️ State Definitions

### 1. DISCOVERED

**Description**: Connector has been detected but not yet authenticated.

**Entry Conditions:**
- Tool URL/endpoint identified
- Connector type recognized
- No credentials present

**Characteristics:**
- Read-only discovery probes allowed
- No data access
- No operational impact

**Exit Paths:**
- → `AUTHORIZED` (after identity probe succeeds)
- → `BLOCKED` (if discovery probe fails)

**Attestation Events:**
- `connector.discovered`

---

### 2. AUTHORIZED

**Description**: Credentials validated but permissions not yet verified.

**Entry Conditions:**
- Identity probe successful
- Valid authentication token/credentials
- Not yet tested for operational access

**Characteristics:**
- Credentials stored (encrypted)
- Permission scope unknown
- Not yet used for operations

**Exit Paths:**
- → `ACTIVE` (after permission scope probe succeeds)
- → `EXPIRED` (if auth token expires)
- → `BLOCKED` (if authorization fails)

**Attestation Events:**
- `connector.authorized`

**Probes Required:**
- Identity probe ✅
- Permission scope probe ⏭️

---

### 3. ACTIVE

**Description**: Fully operational connector with validated permissions.

**Entry Conditions:**
- Identity probe ✅
- Permission scope probe ✅
- Read probe ✅
- Write probe ✅ (if write required)

**Characteristics:**
- All operations permitted
- Regular health checks active
- Evidence mirroring enabled
- Contribution to operational state

**Exit Paths:**
- → `DEGRADED` (partial failure, some operations fail)
- → `EXPIRED` (credentials expire)
- → `BLOCKED` (external blocking condition)
- → `RETIRED` (intentional decommission)

**Attestation Events:**
- `connector.activated`
- `connector.operation.success` (ongoing)
- `connector.operation.failure` (if any)

**Health Monitoring:**
- Read probe: Every 15 minutes
- Write probe: Every 30 minutes
- Permission scope probe: Every 24 hours
- Identity probe: Every 7 days

---

### 4. DEGRADED

**Description**: Partial functionality; some operations fail but connector not fully down.

**Entry Conditions:**
- Previously `ACTIVE`
- Some probes failing but not all
- Examples:
  - Read succeeds, write fails (read-only degradation)
  - Some endpoints timeout
  - Rate limiting active

**Characteristics:**
- Limited operations allowed
- Fallback to canonical repository for failed operations
- Increased probe frequency (every 5 minutes)
- User notification of degradation

**Exit Paths:**
- → `ACTIVE` (after recovery action succeeds)
- → `EXPIRED` (if auth expires during degradation)
- → `BLOCKED` (if degradation worsens)

**Attestation Events:**
- `connector.degraded` (with failure mode)
- `connector.recovery.attempted`
- `connector.recovery.succeeded` / `connector.recovery.failed`

**Recovery Actions:**
- Retry failed operations with exponential backoff
- Reduce request rate (if rate limited)
- Switch to read-only mode (if write fails)
- Cache and queue operations for later replay

---

### 5. EXPIRED

**Description**: Authentication credentials have expired.

**Entry Conditions:**
- Previously `AUTHORIZED` or `ACTIVE` or `DEGRADED`
- Auth token expired (401/403 errors)
- Refresh token expired or invalid

**Characteristics:**
- No operations allowed
- Cached read data may be available (stale)
- Re-authorization required
- Evidence mirroring paused

**Exit Paths:**
- → `AUTHORIZED` (after re-authentication)
- → `BLOCKED` (if re-auth fails repeatedly)
- → `RETIRED` (if not re-authenticated within 30 days)

**Attestation Events:**
- `connector.expired`
- `connector.reauth.requested`
- `connector.reauth.succeeded` / `connector.reauth.failed`

**Recovery Actions:**
- Prompt user for re-authentication
- Attempt refresh token flow (if supported)
- Fall back to cached data (with staleness warnings)
- Queue operations for replay after re-auth

---

### 6. BLOCKED

**Description**: External or internal blocking condition prevents operation.

**Entry Conditions:**
- Repeated probe failures
- External service blocking (IP ban, account suspended)
- Internal policy violation
- Security incident detected

**Characteristics:**
- All operations blocked
- No probes executed
- Manual intervention required
- Incident logged in attestation trail

**Exit Paths:**
- → `AUTHORIZED` (after unblock and re-authorization)
- → `RETIRED` (if unblock unsuccessful after 90 days)

**Attestation Events:**
- `connector.blocked` (with blocking reason)
- `connector.unblock.attempted`
- `connector.unblock.succeeded` / `connector.unblock.failed`

**Recovery Actions:**
- Investigate blocking cause
- Contact external service support (if external block)
- Resolve policy violations
- Wait for ban expiry
- Switch to alternate connector (if available)

---

### 7. RETIRED

**Description**: Connector intentionally decommissioned and no longer in use.

**Entry Conditions:**
- Manual retirement request
- Prolonged `EXPIRED` state (>30 days)
- Prolonged `BLOCKED` state (>90 days)
- Service discontinued
- Connector replaced by alternative

**Characteristics:**
- No operations allowed
- Credentials removed
- Historical data preserved in repository
- Audit trail preserved
- Cannot be reactivated (must be re-DISCOVERED)

**Exit Paths:**
- None (terminal state)

**Attestation Events:**
- `connector.retired` (with reason)

**Decommission Actions:**
- Archive connector configuration
- Preserve historical evidence in repository
- Remove credentials securely
- Update documentation
- Notify dependent components

---

## 🔍 Probe Specifications

### Identity Probe

**Purpose**: Verify connector identity and basic authentication.

**Execution:**
```python
def identity_probe(connector):
    """Verify connector identity and authentication."""
    try:
        response = connector.get('/api/v1/me')  # or equivalent
        if response.status_code == 200:
            return ProbeResult(
                success=True,
                identity=response.json(),
                timestamp=datetime.now()
            )
        else:
            return ProbeResult(
                success=False,
                error=f"HTTP {response.status_code}",
                timestamp=datetime.now()
            )
    except Exception as e:
        return ProbeResult(
            success=False,
            error=str(e),
            timestamp=datetime.now()
        )
```

**Success Criteria:**
- HTTP 200 response
- Valid identity payload (username, account ID, etc.)
- No authentication errors

**Failure Modes:**
- `401 Unauthorized`: Credentials invalid → EXPIRED
- `403 Forbidden`: Account blocked → BLOCKED
- `Network Error`: Transient → Retry
- `Timeout`: Transient → Retry

---

### Read Probe

**Purpose**: Verify read access to connector data.

**Execution:**
```python
def read_probe(connector):
    """Verify read access to connector."""
    try:
        # Read a known resource or list endpoint
        response = connector.get('/api/v1/projects')  # or equivalent
        if response.status_code == 200:
            return ProbeResult(
                success=True,
                data_count=len(response.json()),
                timestamp=datetime.now()
            )
        else:
            return ProbeResult(
                success=False,
                error=f"HTTP {response.status_code}",
                timestamp=datetime.now()
            )
    except Exception as e:
        return ProbeResult(
            success=False,
            error=str(e),
            timestamp=datetime.now()
        )
```

**Success Criteria:**
- HTTP 200 response
- Valid data payload
- No permission errors

**Failure Modes:**
- `403 Forbidden`: Insufficient permissions → DEGRADED
- `429 Rate Limited`: Slow down → DEGRADED
- `500 Internal Error`: Service issue → DEGRADED
- `Timeout`: Network issue → DEGRADED

---

### Write Probe

**Purpose**: Verify write access to connector (if required).

**Execution:**
```python
def write_probe(connector):
    """Verify write access to connector."""
    try:
        # Create a test resource (e.g., comment, tag)
        test_payload = {
            "name": "DAIOF_health_check",
            "created_by": "sovereign_runtime",
            "timestamp": datetime.now().isoformat()
        }
        response = connector.post('/api/v1/test_resource', json=test_payload)

        if response.status_code in [200, 201]:
            # Clean up test resource
            resource_id = response.json().get('id')
            if resource_id:
                connector.delete(f'/api/v1/test_resource/{resource_id}')

            return ProbeResult(
                success=True,
                timestamp=datetime.now()
            )
        else:
            return ProbeResult(
                success=False,
                error=f"HTTP {response.status_code}",
                timestamp=datetime.now()
            )
    except Exception as e:
        return ProbeResult(
            success=False,
            error=str(e),
            timestamp=datetime.now()
        )
```

**Success Criteria:**
- HTTP 200/201 response
- Resource created successfully
- Resource deleted successfully (cleanup)

**Failure Modes:**
- `403 Forbidden`: Insufficient permissions → DEGRADED (read-only mode)
- `429 Rate Limited`: Slow down → DEGRADED
- `Quota Exceeded`: Limit reached → DEGRADED

---

### Permission Scope Probe

**Purpose**: Verify full scope of permissions available.

**Execution:**
```python
def permission_scope_probe(connector):
    """Verify permission scope."""
    required_scopes = [
        'read:projects',
        'write:tasks',
        'read:users',
        'write:comments'
    ]

    try:
        response = connector.get('/api/v1/me/permissions')
        actual_scopes = response.json().get('scopes', [])

        missing_scopes = [s for s in required_scopes if s not in actual_scopes]

        return ProbeResult(
            success=len(missing_scopes) == 0,
            granted_scopes=actual_scopes,
            missing_scopes=missing_scopes,
            timestamp=datetime.now()
        )
    except Exception as e:
        return ProbeResult(
            success=False,
            error=str(e),
            timestamp=datetime.now()
        )
```

**Success Criteria:**
- All required scopes present
- No scope revocations

**Failure Modes:**
- `Missing Scopes`: Insufficient permissions → DEGRADED or BLOCKED
- `Revoked Scopes`: Re-authorization required → EXPIRED

---

## 📝 Attestation Events

All connector state transitions and probe results are logged to the immutable attestation log.

**Event Schema:**
```python
{
    "event_id": "uuid-v4",
    "event_type": "connector.state_transition",
    "connector_id": "asana-main",
    "connector_type": "asana",
    "timestamp": "2026-05-14T23:47:24.959Z",
    "sequence": 12345,
    "previous_state": "ACTIVE",
    "new_state": "DEGRADED",
    "transition_reason": "Write probe failed: HTTP 403",
    "failure_mode": "write_access_lost",
    "recovery_action": "switch_to_read_only_mode",
    "metadata": {
        "last_successful_write": "2026-05-14T22:30:00.000Z",
        "error_count": 3,
        "retry_after": "2026-05-14T23:52:24.959Z"
    },
    "hash": "sha256-of-event-plus-previous-hash",
    "signature": "alpha_prime_omega"
}
```

**Event Types:**
- `connector.discovered`
- `connector.authorized`
- `connector.activated`
- `connector.degraded`
- `connector.expired`
- `connector.blocked`
- `connector.retired`
- `connector.probe.success`
- `connector.probe.failure`
- `connector.recovery.attempted`
- `connector.recovery.succeeded`
- `connector.recovery.failed`

---

## 🛠️ Recovery Actions

### Recovery Action Matrix

| Failure Mode | State | Recovery Action | Fallback |
|--------------|-------|-----------------|----------|
| Auth expired | EXPIRED | Re-authenticate | Use cached data (read-only) |
| Write fails | DEGRADED | Switch to read-only | Queue writes for later |
| Rate limited | DEGRADED | Reduce request rate, exponential backoff | Cache and replay |
| Network timeout | DEGRADED | Retry with backoff | Use canonical repository |
| Permission revoked | BLOCKED | Request re-authorization | Disable connector |
| Service down | DEGRADED | Poll for recovery | Use canonical repository |
| Account suspended | BLOCKED | Contact support, manual intervention | Disable connector |

---

## 📊 Current Connector Status (2026-05-14)

| Connector | State | Last Verified | Notes |
|-----------|-------|---------------|-------|
| **GitHub** | ACTIVE | 2026-05-14T23:47:24Z | Canonical source (always ACTIVE) |
| **Figma** | ACTIVE | 2026-05-14T10:00:00Z | Visual topology substrate |
| **Asana** | ACTIVE | 2026-05-14T09:00:00Z | Execution backlog substrate |
| **Linear** | EXPIRED | 2026-05-10T15:30:00Z | 401 session expired, re-auth needed |
| **Airtable** | DISCOVERED | 2026-05-14T08:00:00Z | Requires authorization |

---

## ✅ Compliance Requirements

All connector implementations must:
- [ ] Implement all 7 lifecycle states
- [ ] Execute all 4 probe types
- [ ] Log all state transitions to attestation log
- [ ] Provide recovery actions for all failure modes
- [ ] Mirror execution evidence to GitHub repository
- [ ] Maintain state transparency (observable at runtime)
- [ ] Support graceful degradation
- [ ] Preserve audit trail

**Validation**: Run `pytest tests/test_connector_lifecycle.py` to verify compliance.

---

## 📚 Related Documentation

- [Sovereign Agentic Runtime Doctrine](./SOVEREIGN_AGENTIC_RUNTIME_DOCTRINE.md)
- [Execution Evidence Registry](./EXECUTION_EVIDENCE_REGISTRY.md)
- [Metadata Schema](./METADATA_SCHEMA.md)
- [Runtime State Machine](./RUNTIME_STATE_MACHINE.md)

---

**End of Connector Lifecycle Specification v1.0.0**

*Signed: Nguyễn Đức Cường (alpha_prime_omega)*
*Verification: 4287*
*Date: 2026-05-14*
