# Copilot-home GitHub Control Plane — Operator Experience

## Purpose

Turn the organization inventory into an operator-facing control surface that answers five questions without opening every repository:

1. What is this repository for?
2. Is it active, experimental, maintenance-only, or awaiting normalization?
3. Which check is authoritative?
4. What blocks the next safe action?
5. What evidence and rollback path support the decision?

This document defines the product behavior. It does not replace `governance/github_ecosystem_manifest.json`; the manifest remains the source of truth.

## Primary user

**System operator / architect**

- Manages one organization with many heterogeneous repositories.
- Needs evidence-first decisions rather than activity-feed noise.
- Must distinguish official GitHub state, local runtime state, and mirror CI state.
- Works under quota constraints and cannot assume cloud agents are always available.

## Core journey

```text
Organization overview
  -> choose risk/lifecycle filter
  -> inspect one repository card
  -> open evidence drawer
  -> choose one safe next action
  -> review validation and rollback
  -> execute through a scoped pull request
```

## Information architecture

### 1. Organization overview

Show:

- repository count and verification date
- lifecycle distribution
- unresolved normalization count
- repositories with non-main default branches
- repositories with undeclared CI authority
- public repositories with local-path or artifact risk
- current quota-critical repositories

The first screen should expose exceptions, not merely recent activity.

### 2. Repository card

Each card must contain:

| Field | Presentation |
|---|---|
| Repository | Name and visibility |
| Role | Human-readable role label |
| Lifecycle | Text badge plus icon |
| CI authority | One primary gate; mirrors shown separately |
| Default branch | Branch name; exception indicator when not `main` |
| Risk | Low / medium / high with text, not color alone |
| Evidence | Verified / partial / missing |
| Next action | One scoped recommendation |

### 3. Evidence drawer

Progressively disclose:

- source repository metadata
- manifest entry
- related pull requests and issues
- failed checks and whether they are PR-caused or baseline/external
- validation command
- rollback instruction
- last verification date

Do not bury missing evidence. Use the literal label `MISSING_EVIDENCE`.

### 4. Action review

Before mutation, require:

```text
Scope
Evidence
Files or settings changed
Validation
Risk
Rollback
Manifest update required: yes/no
```

Destructive actions such as archive, delete, force-push, history rewrite, or default-branch changes require explicit owner confirmation.

## State model

### Lifecycle

- `active`: production or governance-critical; authority must be declared
- `incubating`: prototype with an explicit target state
- `maintenance`: upstream fork or stable dependency surface
- `needs-normalization`: useful content with unresolved identity, branch, CI, or hygiene drift
- `archive-candidate`: retained reference with no proven active role
- `empty`: placeholder with no content

### Evidence

- `verified-by-github-connector`
- `partial`
- `missing`

### Check classification

- `authoritative-pass`
- `authoritative-fail`
- `mirror-pass`
- `mirror-fail`
- `baseline-fail`
- `external-pending`
- `quota-blocked`

A mirror failure must not visually override an authoritative local PASS, but it must remain visible.

## Visual semantics

- Never communicate state with color alone.
- Use a short text label and an icon for every badge.
- Reserve red for an authoritative block or confirmed security risk.
- Use amber for missing evidence, normalization debt, or external pending state.
- Use neutral gray for archived/reference surfaces.
- Keep repository cards compact; place raw hashes, paths, and logs in the evidence drawer.
- Show official GitHub state and local-runtime state in separate labeled groups.

## Accessibility requirements

- Keyboard access for all filters, cards, drawers, and actions.
- Visible focus indicator.
- Minimum 4.5:1 contrast for normal text.
- Status icons must include accessible names.
- Tables require headers and must remain readable at 200% zoom.
- Do not use motion as the only indication of a running check.
- Error messages must state the failed rule and the next corrective action.

## Product acceptance criteria

The operator experience is ready when:

1. All 18 repositories render from the manifest without hand-maintained duplicates.
2. Every active repository displays exactly one authoritative gate.
3. Non-main branches show owner, rationale, exit criteria, and rollback.
4. The overview identifies every `needs-normalization`, `archive-candidate`, and `empty` repository.
5. Missing evidence is visible before any mutation control.
6. No destructive action is offered without explicit confirmation.
7. The UI can distinguish local verifier, GitHub Actions, CircleCI, and upstream checks.
8. The same manifest validation used in CI guards the UI data model.

## Recommended first implementation

Build a read-only static view first:

```text
manifest JSON
  -> validator
  -> generated repository cards
  -> lifecycle / CI / risk filters
  -> evidence drawer
```

Do not add mutation controls until the read-only view matches the manifest and passes accessibility checks.
