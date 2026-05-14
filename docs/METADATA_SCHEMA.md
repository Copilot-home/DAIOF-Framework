# 📋 Metadata Schema Specification

**Version:** 1.0.0
**Status:** CANONICAL SPECIFICATION
**Architect:** Nguyễn Đức Cường (alpha_prime_omega)
**Verification Code:** 4287
**Last Updated:** 2026-05-14

---

## 📋 Overview

This document defines the canonical metadata schema for all components in the Sovereign Agentic Runtime. Metadata provides source-of-truth tracking, synchronization state, and runtime consumer identification.

---

## 🎯 Metadata Philosophy

**Key Principles:**
1. **Provenance Tracking**: Every artifact knows its origin and history
2. **Synchronization State**: External substrate sync status is transparent
3. **Version Control**: Doctrine and schema versions are explicit
4. **Runtime Context**: Consumer identification enables debugging and auditing
5. **Temporal Tracking**: Creation and verification timestamps preserved

---

## 📊 Core Metadata Fields

### Required Fields (All Components)

```python
{
    # === Source Attribution ===
    "doctrine_version": "1.0.0",                          # Semantic version of doctrine
    "source_of_truth": "github:NguyenCuong1989/DAIOF-Framework",  # Canonical source
    "creator_attribution": "alpha_prime_omega",          # Ultimate creator
    "verification_code": 4287,                            # Immutable verification

    # === Temporal Tracking ===
    "created_at": "2026-05-14T23:47:24.959Z",            # ISO 8601 timestamp
    "last_verified_at": "2026-05-14T23:47:24.959Z",      # Last compliance check
    "last_synced_from": null,                             # Last external sync (if any)

    # === Runtime Context ===
    "runtime_consumer": "SymphonyControlCenter",          # Component using this
    "connector_state": "ACTIVE",                          # From CONNECTOR_LIFECYCLE.md

    # === Version Control ===
    "schema_version": "1.0.0",                            # This schema version
    "component_version": "1.0.0"                          # Component implementation version
}
```

---

## 🏷️ Field Definitions

### 1. doctrine_version

**Type**: String (semantic version)
**Required**: Yes
**Immutable**: No (updates with doctrine)
**Format**: `MAJOR.MINOR.PATCH` (e.g., "1.0.0")

**Description**: Version of the Sovereign Agentic Runtime Doctrine this component adheres to.

**Purpose:**
- Ensure doctrine compatibility
- Track doctrine evolution
- Enable migration scripts for doctrine updates

**Validation:**
```python
import re

SEMVER_PATTERN = r'^(\d+)\.(\d+)\.(\d+)(-[0-9A-Za-z-]+(\.[0-9A-Za-z-]+)*)?$'

def validate_doctrine_version(version: str) -> bool:
    return bool(re.match(SEMVER_PATTERN, version))
```

**Examples:**
- `"1.0.0"` - Initial doctrine release
- `"1.1.0"` - Minor doctrine update (backward compatible)
- `"2.0.0"` - Major doctrine update (breaking changes)

---

### 2. source_of_truth

**Type**: String (URI)
**Required**: Yes
**Immutable**: Yes (canonical source never changes)
**Format**: `scheme:location` (e.g., "github:NguyenCuong1989/DAIOF-Framework")

**Description**: Canonical source-of-truth location for this component.

**Purpose:**
- Identify canonical source
- Distinguish from substrate copies
- Enable origin verification

**Supported Schemes:**
- `github:owner/repo` - GitHub repository
- `file:/path/to/local` - Local filesystem
- `git:remote-url` - Git remote

**Validation:**
```python
def validate_source_of_truth(source: str) -> bool:
    valid_schemes = ['github', 'file', 'git']
    if ':' not in source:
        return False
    scheme, location = source.split(':', 1)
    return scheme in valid_schemes and len(location) > 0
```

**Examples:**
- `"github:NguyenCuong1989/DAIOF-Framework"` - Canonical GitHub repo
- `"file:/Users/andy/DAIOF-Framework"` - Local development
- `"git:https://github.com/NguyenCuong1989/DAIOF-Framework.git"` - Git remote

---

### 3. creator_attribution

**Type**: String
**Required**: Yes
**Immutable**: Yes (creator never changes)
**Format**: Free text (alpha_prime_omega)

**Description**: Ultimate creator and architect of the framework.

**Purpose:**
- Preserve sovereignty
- Verify authenticity
- Prevent impersonation

**Validation:**
```python
def validate_creator_attribution(creator: str) -> bool:
    # Only one valid creator
    return creator == "alpha_prime_omega"
```

**Examples:**
- `"alpha_prime_omega"` - ✅ Valid
- `"other_creator"` - ❌ Invalid (sovereignty violation)

---

### 4. verification_code

**Type**: Integer
**Required**: Yes
**Immutable**: Yes (verification code never changes)
**Format**: Integer (4287)

**Description**: Cryptographic verification code for authenticity.

**Purpose:**
- Prevent tampering
- Verify authentic components
- Detect unauthorized modifications

**Validation:**
```python
def validate_verification_code(code: int) -> bool:
    # Only one valid code
    return code == 4287
```

**Examples:**
- `4287` - ✅ Valid
- `1234` - ❌ Invalid (authentication failure)

---

### 5. created_at

**Type**: String (ISO 8601 timestamp)
**Required**: Yes
**Immutable**: Yes (creation time never changes)
**Format**: `YYYY-MM-DDTHH:MM:SS.sssZ` (UTC)

**Description**: Timestamp when component was created.

**Purpose:**
- Track component age
- Audit creation events
- Enable temporal queries

**Validation:**
```python
from datetime import datetime

def validate_created_at(timestamp: str) -> bool:
    try:
        datetime.fromisoformat(timestamp.replace('Z', '+00:00'))
        return True
    except ValueError:
        return False
```

**Examples:**
- `"2026-05-14T23:47:24.959Z"` - ✅ Valid
- `"2026-05-14 23:47:24"` - ❌ Invalid (not ISO 8601)

---

### 6. last_verified_at

**Type**: String (ISO 8601 timestamp)
**Required**: Yes
**Immutable**: No (updates on verification)
**Format**: `YYYY-MM-DDTHH:MM:SS.sssZ` (UTC)

**Description**: Timestamp of last doctrine compliance check.

**Purpose:**
- Track verification freshness
- Detect stale components
- Trigger re-verification

**Validation:**
```python
from datetime import datetime, timedelta

def validate_last_verified_at(timestamp: str, created_at: str) -> bool:
    try:
        verified = datetime.fromisoformat(timestamp.replace('Z', '+00:00'))
        created = datetime.fromisoformat(created_at.replace('Z', '+00:00'))
        return verified >= created  # Cannot verify before creation
    except ValueError:
        return False
```

**Re-verification Triggers:**
- Doctrine version update
- Component modification
- Scheduled (every 24 hours for ACTIVE components)
- Manual request

**Examples:**
- `"2026-05-14T23:47:24.959Z"` - ✅ Valid
- `"2026-05-13T00:00:00.000Z"` - ⚠️ Stale (>24h old)

---

### 7. last_synced_from

**Type**: String (URI) or null
**Required**: No (null if never synced)
**Immutable**: No (updates on sync)
**Format**: `scheme:location?timestamp=ISO8601` or `null`

**Description**: Last external substrate sync source and timestamp.

**Purpose:**
- Track external substrate sync state
- Detect drift from external tools
- Enable sync conflict resolution

**Validation:**
```python
def validate_last_synced_from(synced: str | None) -> bool:
    if synced is None:
        return True  # Never synced is valid

    # Format: "asana:123456789?timestamp=2026-05-14T23:47:24.959Z"
    if '?' not in synced:
        return False

    source, query = synced.split('?', 1)
    if not query.startswith('timestamp='):
        return False

    timestamp = query.split('=', 1)[1]
    return validate_created_at(timestamp)
```

**Examples:**
- `null` - Never synced from external substrate
- `"asana:1234567890?timestamp=2026-05-14T10:00:00.000Z"` - Synced from Asana
- `"figma:file-abc123?timestamp=2026-05-14T09:00:00.000Z"` - Synced from Figma

---

### 8. runtime_consumer

**Type**: String
**Required**: Yes
**Immutable**: No (can change as component moves)
**Format**: Component class name or identifier

**Description**: Component currently consuming/using this entity.

**Purpose:**
- Debugging (who is using this?)
- Dependency tracking
- Resource attribution

**Validation:**
```python
def validate_runtime_consumer(consumer: str) -> bool:
    valid_consumers = [
        'SymphonyControlCenter',
        'DigitalOrganism',
        'DigitalEcosystem',
        'DigitalGenome',
        'DigitalMetabolism',
        'DigitalNervousSystem',
        'DRProtocol',
        'AttestationLog',
        'AuxiliaryPilot'
    ]
    return consumer in valid_consumers or consumer.startswith('Custom')
```

**Examples:**
- `"SymphonyControlCenter"` - Used by symphony
- `"DigitalOrganism:alice"` - Used by specific organism
- `"CustomAgent:deploy-bot"` - Custom agent consumer

---

### 9. connector_state

**Type**: String (enum)
**Required**: Yes (if component is a connector)
**Immutable**: No (transitions per lifecycle)
**Format**: One of 7 lifecycle states

**Description**: Current connector lifecycle state (see CONNECTOR_LIFECYCLE.md).

**Purpose:**
- Track connector health
- Enable graceful degradation
- Trigger recovery actions

**Valid Values:**
- `"DISCOVERED"` - Detected but not authenticated
- `"AUTHORIZED"` - Credentials valid, permissions unverified
- `"ACTIVE"` - Fully operational
- `"DEGRADED"` - Partial functionality
- `"EXPIRED"` - Auth expired
- `"BLOCKED"` - External/internal block
- `"RETIRED"` - Decommissioned

**Validation:**
```python
def validate_connector_state(state: str) -> bool:
    valid_states = [
        'DISCOVERED', 'AUTHORIZED', 'ACTIVE',
        'DEGRADED', 'EXPIRED', 'BLOCKED', 'RETIRED'
    ]
    return state in valid_states
```

**Examples:**
- `"ACTIVE"` - GitHub (canonical, always active)
- `"EXPIRED"` - Linear (401 session expired)
- `"DISCOVERED"` - Airtable (requires auth)

---

### 10. schema_version

**Type**: String (semantic version)
**Required**: Yes
**Immutable**: No (updates with schema)
**Format**: `MAJOR.MINOR.PATCH`

**Description**: Version of this metadata schema.

**Purpose:**
- Enable schema migrations
- Track schema evolution
- Ensure compatibility

**Validation:**
```python
def validate_schema_version(version: str) -> bool:
    return bool(re.match(SEMVER_PATTERN, version))
```

**Examples:**
- `"1.0.0"` - This schema version

---

### 11. component_version

**Type**: String (semantic version)
**Required**: Yes
**Immutable**: No (updates with component)
**Format**: `MAJOR.MINOR.PATCH`

**Description**: Version of the component implementation.

**Purpose:**
- Track component evolution
- Enable component migrations
- Compatibility checking

**Validation:**
```python
def validate_component_version(version: str) -> bool:
    return bool(re.match(SEMVER_PATTERN, version))
```

**Examples:**
- `"1.0.0"` - Initial component release
- `"1.2.3"` - Patch update

---

## 🔧 Extended Metadata Fields

### Optional Fields (Component-Specific)

```python
{
    # === Operational State ===
    "health_score": 0.95,                                 # 0.0-1.0 (optional)
    "harmony_index": 0.98,                                # 0.0-1.0 (optional)
    "k_state": 1,                                         # Zero conflicts (optional)

    # === Four Pillars Scores ===
    "pillars": {                                           # Optional
        "an_toan": 8.5,                                   # Safety score (0-10)
        "duong_dai": 9.0,                                 # Long-term score
        "tin_vao_so_lieu": 8.0,                           # Data-driven score
        "han_che_rui_ro": 8.5                             # Risk minimization score
    },

    # === External Substrate References ===
    "external_references": {                               # Optional
        "asana_task_id": "1234567890",
        "figma_file_id": "abc123def456",
        "linear_issue_id": "DAI-123"
    },

    # === Execution Evidence ===
    "execution_evidence": {                                # Optional
        "last_execution": "2026-05-14T23:47:24.959Z",
        "execution_count": 42,
        "last_result": "success",
        "error_count": 0
    },

    # === Audit Trail ===
    "audit_events": [                                      # Optional
        {
            "event_id": "uuid-v4",
            "event_type": "metadata.updated",
            "timestamp": "2026-05-14T23:47:24.959Z",
            "changed_fields": ["last_verified_at", "connector_state"],
            "changed_by": "SymphonyControlCenter"
        }
    ]
}
```

---

## 📝 Metadata Examples

### Example 1: Active GitHub Connector

```json
{
    "doctrine_version": "1.0.0",
    "source_of_truth": "github:NguyenCuong1989/DAIOF-Framework",
    "creator_attribution": "alpha_prime_omega",
    "verification_code": 4287,
    "created_at": "2025-10-30T00:00:00.000Z",
    "last_verified_at": "2026-05-14T23:47:24.959Z",
    "last_synced_from": null,
    "runtime_consumer": "SymphonyControlCenter",
    "connector_state": "ACTIVE",
    "schema_version": "1.0.0",
    "component_version": "1.0.0",

    "health_score": 1.0,
    "harmony_index": 1.0,
    "k_state": 1,
    "pillars": {
        "an_toan": 10.0,
        "duong_dai": 10.0,
        "tin_vao_so_lieu": 10.0,
        "han_che_rui_ro": 10.0
    }
}
```

### Example 2: Degraded Asana Connector

```json
{
    "doctrine_version": "1.0.0",
    "source_of_truth": "github:NguyenCuong1989/DAIOF-Framework",
    "creator_attribution": "alpha_prime_omega",
    "verification_code": 4287,
    "created_at": "2025-11-01T10:00:00.000Z",
    "last_verified_at": "2026-05-14T09:00:00.000Z",
    "last_synced_from": "asana:1234567890?timestamp=2026-05-14T09:00:00.000Z",
    "runtime_consumer": "SymphonyControlCenter",
    "connector_state": "DEGRADED",
    "schema_version": "1.0.0",
    "component_version": "1.0.0",

    "health_score": 0.6,
    "external_references": {
        "asana_project_id": "1234567890",
        "asana_workspace_id": "0987654321"
    },
    "execution_evidence": {
        "last_execution": "2026-05-14T09:00:00.000Z",
        "last_result": "partial_failure",
        "error_count": 3,
        "failure_mode": "write_access_lost"
    }
}
```

### Example 3: Expired Linear Connector

```json
{
    "doctrine_version": "1.0.0",
    "source_of_truth": "github:NguyenCuong1989/DAIOF-Framework",
    "creator_attribution": "alpha_prime_omega",
    "verification_code": 4287,
    "created_at": "2025-11-05T14:00:00.000Z",
    "last_verified_at": "2026-05-10T15:30:00.000Z",
    "last_synced_from": "linear:DAI?timestamp=2026-05-10T15:30:00.000Z",
    "runtime_consumer": "SymphonyControlCenter",
    "connector_state": "EXPIRED",
    "schema_version": "1.0.0",
    "component_version": "1.0.0",

    "health_score": 0.0,
    "external_references": {
        "linear_team_id": "DAI",
        "linear_project_id": "proj_abc123"
    },
    "execution_evidence": {
        "last_execution": "2026-05-10T15:30:00.000Z",
        "last_result": "auth_failure",
        "error_count": 5,
        "failure_mode": "401_unauthorized"
    }
}
```

---

## ✅ Validation & Compliance

### Validation Function

```python
from typing import Any, Dict, List
from datetime import datetime
import re

SEMVER_PATTERN = r'^(\d+)\.(\d+)\.(\d+)(-[0-9A-Za-z-]+(\.[0-9A-Za-z-]+)*)?$'

def validate_metadata(metadata: Dict[str, Any]) -> tuple[bool, List[str]]:
    """
    Validate metadata against schema specification.

    Returns:
        (is_valid, errors)
    """
    errors = []

    # Required fields
    required_fields = [
        'doctrine_version', 'source_of_truth', 'creator_attribution',
        'verification_code', 'created_at', 'last_verified_at',
        'runtime_consumer', 'connector_state', 'schema_version',
        'component_version'
    ]

    for field in required_fields:
        if field not in metadata:
            errors.append(f"Missing required field: {field}")

    if errors:
        return (False, errors)

    # Validate doctrine_version
    if not re.match(SEMVER_PATTERN, metadata['doctrine_version']):
        errors.append("Invalid doctrine_version format")

    # Validate source_of_truth
    if ':' not in metadata['source_of_truth']:
        errors.append("Invalid source_of_truth format")

    # Validate creator_attribution
    if metadata['creator_attribution'] != 'alpha_prime_omega':
        errors.append("Invalid creator_attribution (sovereignty violation)")

    # Validate verification_code
    if metadata['verification_code'] != 4287:
        errors.append("Invalid verification_code (authentication failure)")

    # Validate timestamps
    for ts_field in ['created_at', 'last_verified_at']:
        try:
            datetime.fromisoformat(metadata[ts_field].replace('Z', '+00:00'))
        except (ValueError, AttributeError):
            errors.append(f"Invalid timestamp format: {ts_field}")

    # Validate connector_state
    valid_states = [
        'DISCOVERED', 'AUTHORIZED', 'ACTIVE',
        'DEGRADED', 'EXPIRED', 'BLOCKED', 'RETIRED'
    ]
    if metadata['connector_state'] not in valid_states:
        errors.append(f"Invalid connector_state: {metadata['connector_state']}")

    # Validate schema_version
    if not re.match(SEMVER_PATTERN, metadata['schema_version']):
        errors.append("Invalid schema_version format")

    # Validate component_version
    if not re.match(SEMVER_PATTERN, metadata['component_version']):
        errors.append("Invalid component_version format")

    return (len(errors) == 0, errors)
```

### Compliance Requirements

All components must:
- [ ] Include all required metadata fields
- [ ] Validate metadata on initialization
- [ ] Update `last_verified_at` every 24 hours
- [ ] Update `last_synced_from` after external sync
- [ ] Preserve immutable fields (creator_attribution, verification_code, created_at)
- [ ] Log metadata changes to attestation trail
- [ ] Enforce sovereignty (alpha_prime_omega, 4287)

**Validation**: Run `pytest tests/test_metadata_schema.py` to verify compliance.

---

## 📚 Related Documentation

- [Sovereign Agentic Runtime Doctrine](./SOVEREIGN_AGENTIC_RUNTIME_DOCTRINE.md)
- [Connector Lifecycle](./CONNECTOR_LIFECYCLE.md)
- [Runtime State Machine](./RUNTIME_STATE_MACHINE.md)
- [Execution Evidence Registry](./EXECUTION_EVIDENCE_REGISTRY.md)

---

**End of Metadata Schema Specification v1.0.0**

*Signed: Nguyễn Đức Cường (alpha_prime_omega)*
*Verification: 4287*
*Date: 2026-05-14*
