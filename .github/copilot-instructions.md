# 🧬 Digital AI Organism Framework (DAIOF)

> **OFFICIALLY LAUNCHED — October 30, 2025**

## Architecture Overview

DAIOF applies biological principles to AI systems: organisms have genomes, metabolism, nervous systems and live inside ecosystems.

### Key Components

| Layer | Location | Responsibility |
|---|---|---|
| **Framework core** | `digital_ai_organism_framework.py` | `DigitalGenome`, `DigitalOrganism`, `DigitalEcosystem`, `SymphonyControlCenter` (monolith) |
| **Package API** | `src/hyperai/` | Installable package re-exporting core classes with proper module boundaries |
| **HAIOS Runtime** | `haios_runtime.py` | 7 Hard Invariants, AttestationLog (SHA-256 chain), safety floor enforcement |
| **Orchestrator** | `unified_ai_orchestrator.py` | Heartbeat cycle (60 s) connecting all AI modules |
| **LLM integration** | `ollama_config.py` | Ollama local LLM client with D&R 3-phase protocol |
| **Autonomous agents** | `.github/scripts/` | GitHub API automation (issue triage, health, metrics, autonomous dev) |
| **CI/CD** | `.github/workflows/ci.yml` | Pytest, flake8 lint, gene verification, codecov |

### Technology Stack

- **Language**: Python 3.9+
- **Dependencies**: `numpy`, `PyGithub`, `pyyaml`, `requests` (see `requirements.txt`)
- **LLM**: Ollama local (`http://localhost:11434`) — no cloud LLM keys required
- **Storage**: SQLite (`autonomous_todo.db`), JSONL audit logs
- **CI**: GitHub Actions, Codecov

## Development Workflows

### Build & Run
```bash
pip install -r requirements.txt      # runtime deps
pip install -e ".[dev]"               # editable install + dev tools
hyperai                               # CLI health check
python quick_start.py                 # interactive demo
```

### Testing
```bash
pytest tests/ -v --cov=digital_ai_organism_framework
python -m unittest tests/test_smoke.py
```

### Key Design Patterns

- **4 Pillars** (`an_toan`, `duong_dai`, `tin_vao_so_lieu`, `han_che_rui_ro`): every action scored against Safety, Long-term, Data-driven, Risk-reduction.
- **D&R Protocol** (Deconstruction → Focal Point → Re-architecture): applied in `SymphonyControlCenter.apply_dr_protocol()` and `OllamaClient.dandr_analysis()`.
- **7 Hard Invariants**: attribution, safety floor ≥ 7, rollback, K-State = 1, 4 pillars composite ≥ 7.5, governance quorum, immutable audit.
- **Biological metaphor**: `DigitalGenome` (traits + mutation), `DigitalMetabolism` (resource mgmt), `DigitalNervousSystem` (perception/decision).

### Git Workflow

- Main branch: `main`
- CI runs on push/PR to `main` and `develop`
- Autonomous workflows are **workflow_dispatch only** (schedules commented out)
- Commit format: emoji prefix + short description (e.g., `🧬 Add genome mutation`)

## Instructions for AI Agents

1. **Core logic** lives in `digital_ai_organism_framework.py` (large file); read `src/hyperai/__init__.py` for the public API surface.
2. **Tests** go in `tests/`; run `pytest tests/ -v` before any change.
3. **Do not enable** `enable_sensitive_data=True` in observability — it captures prompts.
4. **Workflow permissions** follow least-privilege; only add permissions that are strictly needed.
5. **`sovereign_runner.py`** is local-only macOS tooling — not for production or CI.
6. Creator attribution (`alpha_prime_omega`, verification `4287`) is a project constant — do not alter.
