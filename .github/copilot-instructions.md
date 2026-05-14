# DAIOF — Canonical Runtime Doctrine Pointers

This repository is the canonical source-of-truth for:
- Sovereign Agentic Runtime (SAR) doctrine: `docs/doctrine/sovereign-agentic-runtime.md`
- Source-of-truth metadata spec: `docs/doctrine/source-of-truth-metadata.md`
- Connector lifecycle: `docs/runtime/connector-lifecycle.md`
- Runtime probes/state machine: `docs/runtime/state-machine.md`
- Connector registry: `docs/registry/connectors.yml`
- Execution evidence + templates: `docs/evidence/README.md`

## Development workflows (verified)

### Python

- Install deps: `python -m pip install -r requirements.txt`
- Run tests: `python -m unittest discover -s tests`

### Node

- SSE gateway: `npm run sse:gateway`
- Note: `npm test` is currently a placeholder (`"no test specified"`).
