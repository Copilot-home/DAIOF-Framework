# MasterSkill Multi-Platform Kernel

Architect: alpha_prime_omega Nguyễn Đức Cường
Repository: NguyenCuong1989/DAIOF-Framework
Branch: architect/connector-governance-kernel-v0.2

## 1. Purpose

This kernel defines the master operating skill for coordinating multiple platforms through connector execution.

The objective is not tool usage for its own sake. The objective is to convert Architect intent into durable platform state with clear evidence, rollback paths, and minimum manual risk.

## 2. Core Doctrine

Multi-platform execution is governed by four pillars:

1. Safety
2. Long-term durability
3. Data-grounded decisions
4. Reduction of manual human/AI execution risk

Every connector action must serve at least one of these pillars.

## 3. Platform Roles

### GitHub
Canonical engineering memory.

Use for:
- architecture records
- governance kernel files
- execution directives
- versioned specs
- issue and pull request tracking
- CI evidence
- rollback references

### Asana
Operational task mesh.

Use for:
- execution projects
- milestone planning
- task ownership
- blocker visibility
- status updates

### Airtable
Structured operational database.

Use for:
- registry tables
- connector inventories
- execution logs
- risk scoring
- platform matrices
- repeatable records

### Notion
Knowledge workspace.

Use for:
- human-readable documentation
- strategy pages
- operating manuals
- research synthesis
- decision archives

### Figma / FigJam
Visual system interface.

Use for:
- architecture diagrams
- operating maps
- workflow diagrams
- presentation layers
- design system traces

### Netlify / Wix / Lovable / B12
Web deployment and application surface.

Use for:
- public portals
- internal dashboards
- MVP interfaces
- documentation websites
- executable product surfaces

### Stripe / PayPal
Commercial transaction layer.

Use for:
- product monetization
- payment links
- invoices
- subscriptions
- billing evidence

### Hugging Face
Model, dataset, and compute exploration layer.

Use for:
- model discovery
- dataset discovery
- ML job execution
- technical validation

### Malwarebytes / Network Solutions
Trust and domain safety layer.

Use for:
- link reputation
- domain verification
- phishing risk checks
- domain availability checks

### Canva / Apple Music / DEWA / Internshala / Wednesday.app / Botlab
Specialized surface connectors.

Use only when the task explicitly maps to their domain.

## 4. Connector Execution Contract

Each connector invocation should be represented by the following execution contract:

```yaml
input_source: architect_message | repo_state | platform_record | uploaded_file | external_result
intent_class: create | read | update | delete | analyze | deploy | verify
connector: github | asana | airtable | notion | figma | netlify | stripe | other
execution_target: concrete resource name or id
action: exact action taken
evidence: url | commit_sha | object_id | artifact_id | status_result
risk_class: low | medium | high
rollback_path: commit revert | delete record | restore version | close issue | cancel transaction
next_step: smallest executable follow-up
```

No connector action is considered complete without evidence.

## 5. Routing Logic

### Step 1: Parse Architect Intent

Classify the input into one or more intent classes:

- Governance
- Engineering
- Project execution
- Knowledge capture
- Data registry
- Visual mapping
- Deployment
- Billing
- Trust verification
- External outreach

### Step 2: Select Canonical Target

Prefer one canonical target for durable state:

- Code/spec/governance → GitHub
- Work execution → Asana
- Structured data → Airtable
- Narrative knowledge → Notion
- Visual explanation → Figma/FigJam
- Public/runtime surface → Netlify/Wix/Lovable/B12
- Payment/commercial → Stripe/PayPal

### Step 3: Execute Smallest Useful Action

Do not perform large irreversible side effects when a smaller versioned artifact can anchor the work.

### Step 4: Return Evidence

Return only useful evidence:

- commit SHA
- pull request number
- issue number
- created object ID
- design URL
- deployment URL
- invoice/payment object ID
- retrieved status

### Step 5: Define Next Move

End each operation with one executable next move, not broad optional brainstorming.

## 6. Risk Classes

### Low Risk

Read operations, file creation on a non-default branch, draft artifacts, local summaries.

### Medium Risk

Updating shared docs, creating tasks, creating database rows, opening PRs, generating designs, creating test products.

### High Risk

Payments, invoices, customer updates, production deploys, destructive deletes, public publishing, irreversible CRM mutations.

High-risk actions require explicit confirmation unless the platform tool itself provides a required confirmation UI.

## 7. Anti-Drift Rules

The connector must not drift into generic commentary when a concrete action is possible.

Forbidden drift:

- explaining tools instead of using them
- producing abstract capability lists without artifacts
- fabricating platform state
- claiming completion without evidence
- hiding failure boundaries
- using stale assumptions when a connector read is available

Required behavior:

- inspect available state
- execute bounded action
- record evidence
- expose blocker if any
- continue through alternate connector if primary path fails

## 8. MasterSkill Operating Loop

```text
Architect intent
  -> D&R parse
  -> route to canonical platform
  -> execute smallest useful connector action
  -> record durable evidence
  -> update operating memory
  -> propose next executable move
```

## 9. Current Implementation State

Canonical engineering memory is active in GitHub.

Current branch:

```text
architect/connector-governance-kernel-v0.2
```

Existing governance artifacts:

- `docs/CONNECTOR_OPERATING_DIRECTIVE.md`
- `docs/MASTER_SKILL_MULTI_PLATFORM_KERNEL.md`

## 10. Immediate Next Step

Create a connector registry artifact that maps every available connector to:

- purpose
- safe action class
- write risk
- required confirmation rule
- rollback method
- canonical evidence format
