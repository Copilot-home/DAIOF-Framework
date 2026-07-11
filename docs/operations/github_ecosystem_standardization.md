# Copilot-home GitHub Ecosystem Standardization

## Status

- **Topology version**: `1.0.0`
- **Source of truth**: `governance/github_ecosystem_manifest.json`
- **Mutation policy**: Pull request only
- **Verification date**: 2026-07-11
- **Inventory source**: Authenticated GitHub connector

## Purpose

This document converts Copilot-home from an emergent set of repositories into a governed ecosystem with explicit repository roles, lifecycle states, CI authority, evidence status, and normalization work.

The manifest is descriptive first. It does not silently archive repositories, rewrite history, change default branches, or delete files. Every mutation must be scoped, reviewable, reversible, and linked to evidence.

## Non-negotiable invariants

1. **One authoritative gate per repository**
   - Each active repository MUST declare exactly one `ci_authority`.
   - Secondary CI systems MAY mirror results, but MUST NOT create conflicting pass/fail authority.
   - For DAIOF runtime work, the local verifier remains authoritative until a replacement is explicitly approved.

2. **Pull-request-only mutation**
   - No direct default-branch mutation for normalization work.
   - No force push, destructive reset, or history rewrite.
   - Every change must include scope, validation, risk, and rollback notes.

3. **No secrets in repositories**
   - Credentials, tokens, cookies, `auth.json`, `.env`, private key material, and generated secret-bearing artifacts are prohibited.
   - Secret-like paths must be blocked from automated commits.

4. **No local absolute paths in public artifacts**
   - Public repositories MUST use placeholders such as `${HOME}`, `<workspace_root>`, or documented environment variables.
   - Local runtime receipts may exist only in private repositories or in sanitized form.

5. **Repository identity must match content**
   - README, package metadata, badges, links, and descriptions MUST identify the actual repository role.
   - Forks, mirrors, derivatives, and experiments MUST declare that status explicitly.

6. **Default branch discipline**
   - `main` is the default unless an upstream or migration exception is documented.
   - Exceptions such as `canary`, `hyperai_purge`, or `codex/aios-runtime-memory-deploy` require an owner, rationale, exit criteria, and rollback path.

7. **Generated and vendor artifact hygiene**
   - `node_modules`, `.DS_Store`, logs, metrics, `.runtime`, local caches, build output, and generated evidence MUST be ignored unless the repository contract explicitly requires versioned fixtures.

## Lifecycle model

| Lifecycle | Meaning | Mutation rule |
|---|---|---|
| `active` | Production or governance-critical repository | Changes require full validation and rollback plan |
| `incubating` | Prototype with an explicit target state | No release claims without evidence |
| `maintenance` | Upstream fork or stable dependency surface | Track upstream delta and sync policy |
| `needs-normalization` | Active content with identity, branch, CI, or hygiene drift | Fix through scoped PRs before expanding scope |
| `archive-candidate` | Retained reference with no proven active role | Archive only after owner confirmation |
| `empty` | Empty placeholder repository | Define purpose or archive |

## Repository classes

### Core

- `DAIOF-Framework`: canonical governance and runtime source of truth.
- `Alpha`: DAIOF derivative execution node; derivative boundary and artifact hygiene must be normalized.

### Runtime

- `workbench`: private HYPERCORE metadata reasoning engine.
- `HyperAI-Sync`: AIOS runtime memory and restore bridge.
- `hermes-agent`: upstream agent runtime fork.

### Tooling

- `copilot-cli`: terminal and MCP interface.
- `components`: private AI development components and experiments.
- `nguyencuong_2509`: GKE MCP integration fork.
- `literate-robot`: VS Code Python environments extension.

### Workbench

- `vscode`: upstream VS Code workbench base.
- `hyper`: Electron terminal workbench base.

### Product and experiment

- `balancehub-minimal`: governed execution gateway prototype.
- `vite-react`: lightweight UI prototype.
- `trust_of_copilot`: trust and DAIOF derivative research.

### Reference and archive candidates

- `circleci-docs`: upstream CircleCI documentation fork.
- `demo-repository`: GitHub organization demo.
- `miniature-umbrella-demo-repository`: duplicate GitHub organization demo.
- `andy`: empty placeholder.

## Standardization waves

### Wave 0 — Topology lock

- [x] Create authenticated inventory of all 18 accessible repositories.
- [x] Add schema and stdlib validator.
- [x] Declare the central source of truth.
- [ ] Merge the topology PR after review.

### Wave 1 — Critical-path normalization

1. `DAIOF-Framework`
   - Keep `local-verifier` authoritative.
   - Convert GitHub Actions and CircleCI to explicit mirror roles or retire one.
   - Enforce the governance gate before merge.

2. `HyperAI-Sync`
   - Sanitize public absolute paths.
   - Add portable placeholders and environment-variable contracts.
   - Document why the default branch is not `main` and define exit criteria.

3. `copilot-cli`
   - Remove README identity drift and OS artifacts.
   - Select one CI authority.
   - Replace `curl | shell` guidance with checksum-verifiable installation.

4. `Alpha`
   - Declare derivative relationship to DAIOF.
   - Remove generated/vendor artifacts from the default branch.
   - Assign CI authority.

5. `components`
   - Replace the placeholder README with the actual component map.
   - Document the `hyperai_purge` default-branch exception.
   - Assign CI authority.

### Wave 2 — Fork and dependency governance

- `vscode`, `hyper`, `hermes-agent`, `circleci-docs`, `nguyencuong_2509`
  - Record upstream repository and pinned base revision.
  - Generate a fork-delta report.
  - Define sync cadence and conflict policy.
  - Audit install hooks, `postinstall`, git URL dependencies, and network exposure.

### Wave 3 — Product and experiment closure

- `balancehub-minimal`: resolve PR backlog and pin Python dependencies.
- `vite-react`: resolve the open draft PR and name the product owner.
- `trust_of_copilot`: replace copied DAIOF identity with a research-specific README.
- Demo and empty repositories: keep one documented demo or archive redundant placeholders.

## Validation

Run from repository root:

```bash
python3 scripts/validate_github_ecosystem_manifest.py
```

Expected output:

```json
{"status":"PASS","org":"Copilot-home","repository_count":18,"source_of_truth":"github:Copilot-home/DAIOF-Framework"}
```

## Change protocol

Every repository normalization PR must contain:

```text
Scope
Evidence
Files changed
Validation
Risk
Rollback
Manifest update required: yes/no
```

The central manifest must be updated when any of the following changes:

- visibility
- default branch
- lifecycle
- CI authority
- repository role
- public/private local-artifact policy
- archive status
- repository ownership or namespace

## Completion gate

Copilot-home is considered topology-governed when:

1. All 18 repositories have a verified role and lifecycle.
2. Every active repository has exactly one authoritative gate.
3. No public repository contains unresolved absolute local paths or secret-like artifacts.
4. Every fork has an upstream delta and sync policy.
5. Empty and duplicate demo repositories have an explicit retain/archive decision.
6. The manifest validator passes on the default branch.
