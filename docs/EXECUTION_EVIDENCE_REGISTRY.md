# 📊 Execution Evidence Registry

**Version:** 1.0.0
**Status:** CANONICAL SPECIFICATION
**Architect:** Nguyễn Đức Cường (alpha_prime_omega)
**Verification Code:** 4287
**Last Updated:** 2026-05-14

---

## 📋 Overview

This document defines the canonical protocol for mirroring operational evidence from external substrates (Asana, Figma, Linear, Airtable) to the GitHub repository. This ensures the repository remains the source-of-truth and is inspectable, auditable, and recoverable even if external tools drift or fail.

---

## 🎯 Evidence Mirroring Philosophy

**Key Principles:**
1. **GitHub is Canonical**: External tools are substrates, not sources-of-truth
2. **Evidence Preservation**: All operational evidence must be mirrored to repository
3. **Drift Resilience**: Repository remains operational even if external tools fail
4. **Auditability**: All execution history preserved in Git
5. **Recoverability**: System can be reconstructed from repository alone

---

## 🗂️ Evidence Types

### 1. Task Execution Evidence

**Source**: Asana, Linear
**Target**: GitHub Issues + `/evidence/tasks/`

**Data to Mirror**:
- Task title and description
- Creation and completion timestamps
- Assignee and creator
- Status changes and transitions
- Comments and discussions
- Attachments and artifacts
- Dependencies and blockers

**Mirror Format**: JSON + Markdown

```
/evidence/tasks/
├── 2026-05/
│   ├── task_asana_1234567890.json       # Raw JSON from Asana
│   ├── task_asana_1234567890.md         # Human-readable Markdown
│   ├── task_linear_DAI-123.json         # Raw JSON from Linear
│   └── task_linear_DAI-123.md           # Human-readable Markdown
└── README.md                             # Index of all tasks
```

---

### 2. Visual Topology Evidence

**Source**: Figma
**Target**: `/evidence/topology/`

**Data to Mirror**:
- Design file metadata
- Component hierarchy
- Design version history
- Comments and annotations
- Export timestamps
- Visual snapshots (PNG/SVG)

**Mirror Format**: JSON + Images

```
/evidence/topology/
├── figma_file_abc123/
│   ├── metadata.json                     # File metadata
│   ├── components.json                   # Component tree
│   ├── version_history.json              # Version log
│   ├── snapshot_2026-05-14.png           # Visual export
│   └── README.md                         # File documentation
└── README.md                             # Index of all files
```

---

### 3. Data Substrate Evidence

**Source**: Airtable
**Target**: `/evidence/data/`

**Data to Mirror**:
- Base and table metadata
- Record snapshots
- Field definitions
- View configurations
- Automation logs
- Access history

**Mirror Format**: JSON + CSV

```
/evidence/data/
├── airtable_base_xyz789/
│   ├── base_metadata.json                # Base configuration
│   ├── table_projects.csv                # Table export (CSV)
│   ├── table_projects.json               # Table export (JSON)
│   ├── automation_logs.json              # Automation history
│   └── README.md                         # Base documentation
└── README.md                             # Index of all bases
```

---

### 4. Execution Backlog Evidence

**Source**: Asana
**Target**: GitHub Projects + `/evidence/backlog/`

**Data to Mirror**:
- Sprint/project structure
- Task priorities and estimates
- Milestone progress
- Team assignments
- Velocity metrics
- Burndown data

**Mirror Format**: JSON + Markdown

```
/evidence/backlog/
├── sprint_2026-05/
│   ├── sprint_metadata.json              # Sprint configuration
│   ├── tasks.json                        # All tasks in sprint
│   ├── burndown.json                     # Burndown data
│   ├── velocity.json                     # Velocity metrics
│   └── README.md                         # Sprint summary
└── README.md                             # Index of all sprints
```

---

### 5. State Transition Evidence

**Source**: All connectors
**Target**: `/evidence/state_transitions/`

**Data to Mirror**:
- Connector state changes
- Health score history
- Probe results
- Error logs
- Recovery actions

**Mirror Format**: JSON

```
/evidence/state_transitions/
├── connector_github.json                 # GitHub state history
├── connector_asana.json                  # Asana state history
├── connector_figma.json                  # Figma state history
├── connector_linear.json                 # Linear state history
└── connector_airtable.json               # Airtable state history
```

---

## 🔄 Mirroring Protocol

### Sync Frequency

| Evidence Type | Sync Frequency | Trigger |
|---------------|----------------|---------|
| Task Execution | Real-time | Task state change |
| Visual Topology | Daily | Scheduled (00:00 UTC) |
| Data Substrate | Hourly | Scheduled (:00 each hour) |
| Execution Backlog | Daily | Scheduled (06:00 UTC) |
| State Transitions | Real-time | State change event |

### Sync Workflow

```
┌─────────────────────────────────────────────────────────┐
│  External Substrate (e.g., Asana)                       │
│  - Task created                                         │
│  - Task updated                                         │
│  - Task completed                                       │
└────────────────┬────────────────────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────────────────────────┐
│  Connector (e.g., AsanaConnector)                       │
│  - Detect event via webhook/polling                     │
│  - Fetch full event data                                │
│  - Validate data integrity                              │
└────────────────┬────────────────────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────────────────────────┐
│  Evidence Sync Engine                                   │
│  - Transform to canonical format                        │
│  - Enrich with metadata                                 │
│  - Validate against schema                              │
└────────────────┬────────────────────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────────────────────────┐
│  Repository Writer                                      │
│  - Write JSON + Markdown files                          │
│  - Update index files                                   │
│  - Create Git commit                                    │
│  - Push to remote                                       │
└────────────────┬────────────────────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────────────────────────┐
│  Attestation Logger                                     │
│  - Log sync event                                       │
│  - Update connector metadata                            │
│  - Update last_synced_from field                        │
└─────────────────────────────────────────────────────────┘
```

---

## 📝 Evidence Schema

### Task Evidence Schema

```json
{
  "evidence_type": "task_execution",
  "evidence_id": "task_asana_1234567890",
  "source": {
    "substrate": "asana",
    "substrate_id": "1234567890",
    "substrate_url": "https://app.asana.com/0/1234567890/1234567890"
  },
  "metadata": {
    "doctrine_version": "1.0.0",
    "source_of_truth": "github:NguyenCuong1989/DAIOF-Framework",
    "creator_attribution": "alpha_prime_omega",
    "verification_code": 4287,
    "synced_at": "2026-05-14T23:47:24.959Z",
    "schema_version": "1.0.0"
  },
  "task": {
    "title": "Implement connector lifecycle states",
    "description": "Define 7 lifecycle states for connectors...",
    "status": "completed",
    "priority": "high",
    "created_at": "2026-05-10T10:00:00.000Z",
    "completed_at": "2026-05-14T23:00:00.000Z",
    "assignee": "alpha_prime_omega",
    "creator": "alpha_prime_omega",
    "tags": ["infrastructure", "connectors", "doctrine"],
    "dependencies": [],
    "blockers": []
  },
  "history": [
    {
      "timestamp": "2026-05-10T10:00:00.000Z",
      "action": "created",
      "actor": "alpha_prime_omega",
      "details": {"initial_status": "pending"}
    },
    {
      "timestamp": "2026-05-12T14:00:00.000Z",
      "action": "status_changed",
      "actor": "alpha_prime_omega",
      "details": {"from": "pending", "to": "in_progress"}
    },
    {
      "timestamp": "2026-05-14T23:00:00.000Z",
      "action": "status_changed",
      "actor": "alpha_prime_omega",
      "details": {"from": "in_progress", "to": "completed"}
    }
  ],
  "comments": [
    {
      "timestamp": "2026-05-12T14:30:00.000Z",
      "author": "alpha_prime_omega",
      "text": "Starting implementation of 7 states: DISCOVERED, AUTHORIZED, ACTIVE, DEGRADED, EXPIRED, BLOCKED, RETIRED"
    }
  ],
  "attachments": [
    {
      "filename": "connector_state_diagram.png",
      "url": "https://asana.com/attachments/...",
      "mirrored_to": "/evidence/tasks/2026-05/task_asana_1234567890_attachment_1.png"
    }
  ]
}
```

### Visual Topology Evidence Schema

```json
{
  "evidence_type": "visual_topology",
  "evidence_id": "figma_file_abc123",
  "source": {
    "substrate": "figma",
    "substrate_id": "abc123",
    "substrate_url": "https://figma.com/file/abc123/DAIOF-Topology"
  },
  "metadata": {
    "doctrine_version": "1.0.0",
    "source_of_truth": "github:NguyenCuong1989/DAIOF-Framework",
    "creator_attribution": "alpha_prime_omega",
    "verification_code": 4287,
    "synced_at": "2026-05-14T23:47:24.959Z",
    "schema_version": "1.0.0"
  },
  "file": {
    "name": "DAIOF System Topology",
    "description": "Visual representation of component relationships",
    "last_modified": "2026-05-14T12:00:00.000Z",
    "version": "v42",
    "editors": ["alpha_prime_omega"]
  },
  "components": [
    {
      "id": "comp_1",
      "name": "Symphony Control Center",
      "type": "frame",
      "description": "Central orchestrator",
      "connections": ["comp_2", "comp_3", "comp_4"]
    },
    {
      "id": "comp_2",
      "name": "Digital Genome",
      "type": "component",
      "description": "Trait storage",
      "connections": []
    }
  ],
  "exports": [
    {
      "format": "PNG",
      "resolution": "2x",
      "path": "/evidence/topology/figma_file_abc123/snapshot_2026-05-14.png"
    }
  ]
}
```

---

## 🔍 Evidence Verification

### Verification Process

```python
def verify_evidence(evidence_path: str) -> tuple[bool, list[str]]:
    """
    Verify evidence integrity and compliance.

    Returns:
        (is_valid, errors)
    """
    errors = []

    # Load evidence file
    try:
        with open(evidence_path, 'r') as f:
            evidence = json.load(f)
    except Exception as e:
        return (False, [f"Failed to load evidence: {e}"])

    # Verify metadata
    required_metadata = [
        'doctrine_version', 'source_of_truth',
        'creator_attribution', 'verification_code',
        'synced_at', 'schema_version'
    ]

    if 'metadata' not in evidence:
        errors.append("Missing metadata section")
    else:
        for field in required_metadata:
            if field not in evidence['metadata']:
                errors.append(f"Missing metadata field: {field}")

        # Verify sovereignty
        if evidence['metadata'].get('creator_attribution') != 'alpha_prime_omega':
            errors.append("Invalid creator_attribution (sovereignty violation)")

        if evidence['metadata'].get('verification_code') != 4287:
            errors.append("Invalid verification_code (authentication failure)")

    # Verify source reference
    if 'source' not in evidence:
        errors.append("Missing source section")
    else:
        required_source = ['substrate', 'substrate_id', 'substrate_url']
        for field in required_source:
            if field not in evidence['source']:
                errors.append(f"Missing source field: {field}")

    # Verify evidence type
    valid_types = [
        'task_execution', 'visual_topology',
        'data_substrate', 'execution_backlog',
        'state_transition'
    ]
    if evidence.get('evidence_type') not in valid_types:
        errors.append(f"Invalid evidence_type: {evidence.get('evidence_type')}")

    return (len(errors) == 0, errors)
```

---

## 📊 Current Evidence Status (2026-05-14)

| Substrate | Evidence Type | Last Synced | Status | Records |
|-----------|---------------|-------------|--------|---------|
| **Asana** | Task Execution | 2026-05-14 09:00 | ✅ SYNCED | 42 tasks |
| **Asana** | Execution Backlog | 2026-05-14 06:00 | ✅ SYNCED | 3 sprints |
| **Figma** | Visual Topology | 2026-05-14 00:00 | ✅ SYNCED | 5 files |
| **Linear** | Task Execution | 2026-05-10 15:30 | ⚠️ STALE | 12 tasks |
| **Airtable** | Data Substrate | Never | ❌ NOT SYNCED | 0 records |

---

## 🛠️ Evidence Sync Implementation

### Python Implementation Example

```python
from datetime import datetime
from pathlib import Path
import json


class EvidenceSyncEngine:
    """Mirror operational evidence to repository."""

    def __init__(self, repo_path: str):
        self.repo_path = Path(repo_path)
        self.evidence_dir = self.repo_path / 'evidence'

    def sync_task_evidence(self, task_data: dict, source: str):
        """
        Sync task execution evidence from external substrate.

        Args:
            task_data: Raw task data from substrate
            source: Source substrate name (e.g., 'asana', 'linear')
        """
        # Transform to canonical format
        evidence = self._transform_task_evidence(task_data, source)

        # Validate evidence
        is_valid, errors = verify_evidence_dict(evidence)
        if not is_valid:
            raise ValueError(f"Evidence validation failed: {errors}")

        # Determine storage path
        month_dir = self.evidence_dir / 'tasks' / evidence['metadata']['synced_at'][:7]
        month_dir.mkdir(parents=True, exist_ok=True)

        # Write JSON
        json_path = month_dir / f"{evidence['evidence_id']}.json"
        with open(json_path, 'w') as f:
            json.dump(evidence, f, indent=2)

        # Write Markdown (human-readable)
        md_path = month_dir / f"{evidence['evidence_id']}.md"
        self._write_task_markdown(evidence, md_path)

        # Update index
        self._update_task_index(evidence)

        # Git commit
        self._git_commit(
            files=[json_path, md_path],
            message=f"Mirror task evidence: {evidence['task']['title']}"
        )

        # Log to attestation trail
        self._log_sync_event(evidence)

    def _transform_task_evidence(self, task_data: dict, source: str) -> dict:
        """Transform substrate-specific task data to canonical format."""
        return {
            'evidence_type': 'task_execution',
            'evidence_id': f"task_{source}_{task_data['id']}",
            'source': {
                'substrate': source,
                'substrate_id': str(task_data['id']),
                'substrate_url': task_data.get('url', '')
            },
            'metadata': {
                'doctrine_version': '1.0.0',
                'source_of_truth': 'github:NguyenCuong1989/DAIOF-Framework',
                'creator_attribution': 'alpha_prime_omega',
                'verification_code': 4287,
                'synced_at': datetime.utcnow().isoformat() + 'Z',
                'schema_version': '1.0.0'
            },
            'task': {
                'title': task_data.get('name', ''),
                'description': task_data.get('notes', ''),
                'status': task_data.get('status', ''),
                'priority': task_data.get('priority', ''),
                'created_at': task_data.get('created_at', ''),
                'completed_at': task_data.get('completed_at'),
                'assignee': task_data.get('assignee', {}).get('name', ''),
                'creator': task_data.get('creator', {}).get('name', ''),
                'tags': task_data.get('tags', []),
                'dependencies': task_data.get('dependencies', []),
                'blockers': task_data.get('blockers', [])
            },
            'history': task_data.get('history', []),
            'comments': task_data.get('comments', []),
            'attachments': task_data.get('attachments', [])
        }

    def _write_task_markdown(self, evidence: dict, md_path: Path):
        """Write human-readable Markdown summary."""
        task = evidence['task']
        md_content = f"""# {task['title']}

**Status**: {task['status']}
**Priority**: {task['priority']}
**Assignee**: {task['assignee']}
**Created**: {task['created_at']}
**Completed**: {task.get('completed_at', 'In progress')}

## Description

{task['description']}

## Tags

{', '.join(task['tags'])}

## History

"""
        for event in evidence['history']:
            md_content += f"- **{event['timestamp']}**: {event['action']} by {event['actor']}\n"

        md_content += "\n## Comments\n\n"
        for comment in evidence['comments']:
            md_content += f"**{comment['author']}** ({comment['timestamp']}):\n{comment['text']}\n\n"

        md_content += f"\n---\n*Synced from {evidence['source']['substrate']} at {evidence['metadata']['synced_at']}*\n"

        with open(md_path, 'w') as f:
            f.write(md_content)

    def _update_task_index(self, evidence: dict):
        """Update master task index."""
        index_path = self.evidence_dir / 'tasks' / 'README.md'
        # Implementation: Append to index or regenerate
        pass

    def _git_commit(self, files: list, message: str):
        """Create Git commit for evidence."""
        # Implementation: Use GitPython or subprocess
        pass

    def _log_sync_event(self, evidence: dict):
        """Log sync event to attestation trail."""
        # Implementation: Append to attestation log
        pass
```

---

## ✅ Compliance Requirements

All evidence mirroring must:
- [ ] Transform to canonical schema
- [ ] Include required metadata fields
- [ ] Verify sovereignty (alpha_prime_omega, 4287)
- [ ] Store both JSON and human-readable formats
- [ ] Update master index files
- [ ] Create Git commits for traceability
- [ ] Log sync events to attestation trail
- [ ] Handle sync failures gracefully (retry with backoff)

**Validation**: Run `pytest tests/test_evidence_sync.py` to verify compliance.

---

## 🔄 Recovery from Evidence Loss

If external substrates are lost or corrupted:

1. **Repository is Complete**: All evidence preserved in `/evidence/`
2. **Reconstruct External State**: Use evidence files to recreate tasks/data
3. **Attestation Trail Intact**: Full audit history preserved
4. **No Data Loss**: GitHub remains canonical source-of-truth

---

## 📚 Related Documentation

- [Sovereign Agentic Runtime Doctrine](./SOVEREIGN_AGENTIC_RUNTIME_DOCTRINE.md)
- [Connector Lifecycle](./CONNECTOR_LIFECYCLE.md)
- [Metadata Schema](./METADATA_SCHEMA.md)
- [Runtime State Machine](./RUNTIME_STATE_MACHINE.md)

---

**End of Execution Evidence Registry v1.0.0**

*Signed: Nguyễn Đức Cường (alpha_prime_omega)*
*Verification: 4287*
*Date: 2026-05-14*
