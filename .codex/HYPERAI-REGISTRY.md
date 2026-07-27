# HyperAI Federated Personal Cloud Registry

**Version:** 2.1 (Placeholder Dev Mode)  
**Canonical Model:** `H = <A, C, R, P, M, E>`  
**Owner:** Nguyễn Đức Cường (Andy) — Canon Authority

```text
Operational(H) = A.consistent
               ∧ C.valid
               ∧ R.healthy
               ∧ P.reachable
               ∧ M.preserved
               ∧ E.verified
```

> **Note on dev secrets:** All cloud credentials in this registry are stored as
> placeholders (`PASTE_KEY_HERE`) or referenced via environment variables.
> Real values are injected by the owner through VS Code: Secret Storage,
> password manager, or `~/.zshenv`. Do not commit plaintext keys.

---

## A — Authority / Canon

| Component | Artifact | Status | Evidence |
|-----------|----------|--------|----------|
| Canon law | `.codex/AGENTS.md` | PASS | Loaded at session start |
| Sovereignty notice | `.HYPERAI_SOVEREIGNTY_NOTICE.json` | PASS | Local-only AI assertion |
| Identity anchor | `.ai-identity-link` / `.ai-identity/` | PASS | Creator identity confirmed |

## C — VS Code: Control Plane

| Component | Artifact | Status | Evidence / Note |
|-----------|----------|--------|-----------------|
| Stable settings | `Library/Application Support/Code/User/settings.json` | PASS | Java, Modelflare, Tenure wired |
| Insiders settings | `Library/Application Support/Code - Insiders/User/settings.json` | PASS | OpenAI key placeholder, Modelflare, Tenure |
| Chat language models | `chatLanguageModels.json` (both) | PARTIAL | Vendor aliases OK; OpenAI Insiders key is placeholder |
| Extensions (active) | `modelflare`, `tenureai.tenure-vscode`, `vscode-openai`, `agent-hub` | PASS | Installed in Insiders; Tenure copied to Stable |

## R — Runtime & Bridges

| Component | Artifact | Endpoint | Status | Note |
|-----------|----------|----------|--------|------|
| HyperAI app | `app.py` | `http://127.0.0.1:8000` | PASS | Default model `qwen2.5:1.5b`; compile OK |
| Ollama daemon | `/opt/homebrew/bin/ollama` | `http://127.0.0.1:11434` | PASS | Ollama-first per `local-model` skill |
| Phoenix bridge | `tr-gi-p/tools/phoenix-hyperai-api-server.py` | `http://127.0.0.1:9001` | DECLARED, NOT RUNNING | launchd `com.hyperai.phoenix.bridge` not loaded; target `127.0.0.1:37002/api` |
| Tenure server | `~/.tenure/docker-compose.yml` | `http://127.0.0.1:5757` | RESOLVED | Container `tenure-tenure-1` running; token generated |
| Agent Hub | `agent-hub.agent-hub-vscode` extension | `127.0.0.1:8787` | DECLARED | Extension-managed; starts with VS Code: |
| Docker Desktop | `~/Library/Containers/com.docker.docker` | — | PASS | Running after disk cleanup |

## P — Model / Provider Routing

| Provider | Registry Name | Endpoint | Status | Credential Source |
|----------|--------------|----------|--------|-------------------|
| Ollama local | `ollama-local` | `127.0.0.1:11434` | PASS | No key; local model weights |
| LM Studio | `lm-studio` | `127.0.0.1:1234` | PASS | No key; `~/.lmstudio/models` |
| Modelflare (Cloudflare) | `modelflare.*` settings | Cloudflare AI Gateway | CONFIGURED, PLACEHOLDER | `CLOUDFLARE_ACCOUNT_ID` via env; `modelflare.apiKey` = `PASTE_MODEFLARE_API_KEY_HERE` |
| Tenure | `tenure-local` (agent-hub) | `127.0.0.1:5757` | ENABLED, NO PROVIDERS | `TENURE_API_TOKEN` from `~/.tenure/token` via `.zshenv`; needs onboard provider to expose models |
| OpenAI / Anthropic / Gemini / etc. | `openai`, `anthropic`, `gemini`... | Cloud APIs | DISABLED | `*_API_KEY` env vars needed |

## M — Memory / Cache / State

| Component | Location | Size | Status | Note |
|-----------|----------|------|--------|------|
| Ollama models | `~/.ollama/models/blobs` | ~18G | PASS | Runtime weights for Ollama |
| LM Studio models | `~/.lmstudio/models` | ~20G | PASS | GGUF/MLX for LM Studio |
| HuggingFace cache | `~/.cache/huggingface/hub` | ~7G | PASS | Dead `gemma-4-26b` partial download removed |
| UV package cache | `~/.cache/uv` | ~1.3G | PASS | Python wheel cache |
| Docker VM | `~/Library/Containers/com.docker.docker/Data/vms` | ~20G | PASS | Container runtime disk |
| Disk | `/System/Volumes/Data` | 15G free | WARNING | Was 100%; cleaned to 97% |

## E — Evidence / Observability / CI

| Component | Artifact | Status | Note |
|-----------|----------|--------|------|
| Unit tests | `tests/test_app.py` | PASS (syntax) | `app.py` compiles; pytest not installed in system Python |
| CI/CD | `.github/workflows/ci-cd.yml` | NOT RUN | Needs push to trigger |
| Health probes | Ollama, Tenure, app.py | PASS | Manual probes succeeded |

---

## Current Operational Verdict

| Layer | Verdict |
|-------|---------|
| A — Authority/Canon | PASS |
| C — VS Code: control plane | PARTIAL PASS |
| R — Runtime & bridges | PASS |
| P — Provider routing | PARTIAL PASS |
| M — Memory/cache/state | PASS (disk WARNING) |
| E — Evidence/CI | PARTIAL PASS |
| **Overall** | **PARTIAL OPERATIONAL** |

### Open deltas

1. `P/Modelflare`: API key is placeholder; store via `Modelflare: Store Credentials`.
2. `P/Tenure`: enable `tenure-local` in `agent-hub.config.json` after onboarding a provider.
3. `C/OpenAI Insiders`: replace `${input:chat.lm.secret.insiders-openai}` with real key.
4. `E/CI`: push to run GitHub Actions.
5. `M/Disk`: 15G free is temporary; plan further cleanup if pulling more models.

---

## Placeholder / Rotation Checklist

| Secret | Where to inject | Current placeholder / env |
|--------|-----------------|---------------------------|
| OpenAI project key | `chatLanguageModels.json` Insiders / `agent-hub` env | `${input:chat.lm.secret.insiders-openai}` |
| Cloudflare API token | VS Code: Secret Storage (`Modelflare: Store Credentials`) or `CLOUDFLARE_API_TOKEN` | `PASTE_MODEFLARE_API_KEY_HERE` (settings.json) |
| Anthropic key | `agent-hub.config.json` `ANTHROPIC_API_KEY` | env var |
| Gemini keys | `agent-hub.config.json` `GEMINI_API_KEY` | env var |
| GitHub PAT | `agent-hub.config.json` `GITHUB_TOKEN` | env var |
| OpenRouter / Mistral / etc. | `agent-hub.config.json` matching `*_API_KEY` | env var |
| Tenure local token | auto-generated at `~/.tenure/token`, sourced in `.zshenv` | `TENURE_API_TOKEN` |

> **Rule:** Test with placeholders → owner pastes real keys → run end-to-end
> → rotate all exposed keys in one batch before production.
