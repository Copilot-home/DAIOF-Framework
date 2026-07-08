# DAIOF Local CI/CD Runbook

Updated: 2026-07-08

## Purpose

`scripts/local_cicd.py` provides a local-first CI/CD operator for DAIOF runtime work. It is designed to make local automation behave like a controlled workflow runner without blindly pushing, merging, or staging unrelated files.

## Commands

```bash
npm run local:cicd:status
npm run local:cicd:verify
npm run local:cicd:autocommit
npm run local:cicd:automerge
```

Mutation is disabled by default. To commit or merge, pass `--execute` after the npm script separator:

```bash
npm run local:cicd:autocommit -- --execute --message "chore: update local automation"
npm run local:cicd:automerge -- --execute
```

Pushing is a separate explicit gate:

```bash
npm run local:cicd:autocommit -- --execute --push
npm run local:cicd:automerge -- --execute --push
```

## Verification Gate

`local:cicd:verify` runs:

- `node --check apps/sse-gateway/server.mjs`
- `npm test`
- Python compile checks for core runtime files
- `python tools/governance/governance_gate.py validate`
- SSE gateway root endpoint smoke test when port `5000` is free

If port `5000` is already occupied, the direct smoke test is skipped and the Node test suite remains the runtime coverage source.

## Safety Rules

- No `git reset`, no force push, no destructive checkout.
- No mutation without `--execute`.
- No push without `--push`.
- Refuses to commit forbidden runtime/secret/generated paths such as `.env`, `.runtime/`, `logs/`, `metrics/`, `.venv/`, and `node_modules/`.
- Refuses to merge with a dirty working tree.
- Writes proof artifacts to `.runtime/local-cicd/`.

## Intended Local Runtime Loop

```text
status
-> verify
-> autocommit dry-run
-> autocommit --execute
-> automerge dry-run
-> automerge --execute
-> optional --push
```

This keeps DAIOF operational on local runtime while preserving traceability and avoiding blind automation.
