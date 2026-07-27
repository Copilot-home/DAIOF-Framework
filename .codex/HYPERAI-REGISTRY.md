# HyperAI Federated Personal Cloud Registry

**Version:** 3.0 (MacM2 Reconciled)  
**Canonical Model:** `H = <A, C, R, P, M, E>`  
**Owner:** Nguyễn Đức Cường (Andy) — Canon Authority  
**Node:** MacBook Pro Mac14,9 (Apple Silicon) — Sovereign control-and-runtime node

```text
Operational(H) = A.consistent
               ∧ C.valid
               ∧ R.healthy
               ∧ P.reachable
               ∧ M.preserved
               ∧ E.verified

System stability = Lineage integrity
                 ∧ Capacity headroom
                 ∧ Control-state consistency
```

> **Dev-mode secret policy:** All cloud credentials are placeholders (`PASTE_KEY_HERE`)
> or env-var references. Real keys are injected by the owner via VS Code: Secret Storage,
> password manager, or `~/.zshenv`. Do not commit plaintext keys.

---

## A — Authority / Canon

| Component | Artifact | Status | Evidence |
|-----------|----------|--------|----------|
| Canon law | `.codex/AGENTS.md` | PASS | Loaded at session start |
| Workspace Canon | `HyperAI-Sync/AGENTS.md` | PASS | MCP-first / autonomous OODA loaded |
| Sovereignty notice | `.HYPERAI_SOVEREIGNTY_NOTICE.json` | PASS | Local-only AI assertion |
| Identity anchor | `.ai-identity-link` / `.ai-identity/` | PASS | Creator identity confirmed |

---

## C — Control Plane

| Component | Artifact | Role | Status | Evidence |
|-----------|----------|------|--------|----------|
| VS Code: Stable | `Code/User/settings.json` | Interactive / model / tool control surface | PASS | Java, Modelflare, Tenure wired; TCP evidence to Ollama:11434 and LM Studio:1234 |
| VS Code: Insiders | `Code - Insiders/User/settings.json` | Insiders control surface | PASS | OpenAI key placeholder, Modelflare, Tenure |
| Chat language models | `chatLanguageModels.json` (both) | Vendor aliases | PARTIAL | OpenAI Insiders key is placeholder |
| Agent Hub | `agent-hub.agent-hub-vscode` extension | Provider/agent registry plane | DECLARED | `agent-hub.config.json` loaded; starts with VS Code: on port 8787 |
| Launchd | `~/Library/LaunchAgents/*.plist` | Service lifecycle substrate | PASS | Core services loaded/running |
| Extensions | `modelflare`, `tenureai.tenure-vscode`, `vscode-openai`, `agent-hub`, `pieces.os` | Active tool plane | PASS | Installed in Insiders; Tenure copied to Stable |

---

## R — Runtime & Bridges

| Service | LaunchAgent | Entrypoint | Port | Status | Note |
|---------|-------------|------------|------|--------|------|
| HyperAI OS Master | `com.hyperai.os.master` | `workbench/hyperai_os_master.py --daemon` | — | PASS | Survival governor; disk state now `STABLE` |
| Orchestrator | `com.hyperai.orchestrator` | `workbench/agents/run_orchestrator.sh` | — | PASS | One-shot schedule; ran successfully |
| Escalation Agent | `com.hyperai.escalation` | `workbench/agents/escalation_agent.py` | — | PASS | One-shot schedule; ran successfully |
| FinalAI OpenAI Proxy | `com.hyperai.finalai-openai-proxy` | Python proxy | `127.0.0.1:50520` | PASS | Backend `http://192.168.3.158:5052/api/chat/message` |
| Phoenix Bridge | `com.hyperai.phoenix.bridge` | `tr-gi-p/tools/phoenix-hyperai-api-server.py` | `0.0.0.0:9001` | PASS | Health/audit boundary; upstream `50520` OK; Ollama 11434 PASS |
| OpenClaw Gateway | `ai.openclaw.gateway` | Node gateway | `127.0.0.1:18789` | PASS | Bonjour advertised; Kimi bridge connected |
| Vietnamese AI Symphony | `com.vietnamese.ai.symphony.autolauncher` | `vietnamese_ai_symphony_auto_launcher.py` | — | PASS | Running |
| GAM Memory Guard | `com.andy.apo.gam-memory-guard` | `Projects/AI/Tools/ops/drift-memory-guard.sh` | — | PASS | Ran |
| Mesh Control Probe | `com.apomega.meshctl.probe` | `ecosystem_audit/scripts/meshctl.py` | — | PASS | Probe executed |
| Telemetry Router | `com.hyperai.telemetry.router.loop` | `HyperAI-Sync/runtime/telemetry_router/scripts/auto_loop.sh` | — | PASS | Loop running |
| HyperAI Startup | `com.hyperai.startup` | `.hyperai/services/login_startup_wrapper.sh` | — | PASS | Consciousness + process manager started |
| Clawbot Metrics | `com.hyperai.clawbot.metrics` | `scripts/clawbot_hyperai_metrics.sh` | — | PASS | Ran |
| Ollama | launchd + app | `/opt/homebrew/bin/ollama` | `*:11434` | PASS | Ollama-first; multiple local models |
| LM Studio | `lms server start` | `llmster` | `127.0.0.1:1234` | PASS | Server started on demand |
| Tenure Server | `~/.tenure/docker-compose.yml` | Docker compose | `0.0.0.0:5757` | PASS | Container `tenure-tenure-1` + Mongo; token generated |
| Redis | `homebrew.mxcl.redis` | `redis-server` | `127.0.0.1:6379` | PASS | Local state/cache |
| Pieces OS | `com.pieces.os.launch` | Pieces OS | — | PASS | Running |
| Docker Desktop | — | `com.docker.docker` | — | PASS | VM running; image/volume prune reclaimed ~13GB |
| Code-Server | `homebrew.mxcl.code-server` | code-server | — | OFF | Not loaded |
| Registry Dashboard | `com.hyperai.registry.dashboard` | `python3 -m http.server 8765` | `127.0.0.1:8765` | FAILED | WorkingDir `/Volumes/External/...` unavailable |
| Connector Watchdog | `com.hyperai.connector.watchdog` | `/Volumes/External/.../hyperai_connector_watchdog.sh` | — | FAILED | External volume unavailable |
| DAIOF CloudSync | `com.daiof.cloudsync` | `cloud_ecosystem_storage/bin/sync_all.sh` | — | FAILED | Google Drive `rclone` token expired |

### Runtime chain

```text
VS Code / Agent Hub
        ↓
Launchd lifecycle substrate
        ↓
  OS Master ──survival governor
  Orchestrator ──index/doc/todo regeneration
  Escalation ──48h scan
  FinalAI :50520 ──OpenAI-compatible proxy ──→ LAN backend :5052
  Phoenix :9001 ──health/audit boundary ──→ FinalAI :50520
  OpenClaw :18789 ──gateway/IM bridge
  Ollama :11434
  LM Studio :1234
  Tenure :5757
  Redis :6379
  Docker / Tenure / Mongo
```

---

## P — Model / Provider Routing

```text
Model plane
├─ Local execution
│  ├─ Ollama :11434
│  ├─ LM Studio :1234
│  ├─ Qwen, Llama, all-minilm, nomic-embed-text
│  └─ embedding models
├─ Local gateways
│  ├─ Phoenix :9001
│  ├─ FinalAI :50520
│  ├─ OpenClaw :18789
│  └─ Agent Hub :8787 (VS Code: extension)
└─ Remote / provider references
   ├─ Cloudflare / Modelflare (placeholder)
   ├─ Tenure :5757 (enabled, needs provider onboard)
   └─ Cloud vendor aliases in Ollama (kimi, gemini, minimax, qwen-coder)
```

| Provider | Registry Name | Endpoint | Status | Credential Source |
|----------|--------------|----------|--------|-------------------|
| Ollama local | `ollama-local` | `127.0.0.1:11434` | PASS | No key; local model weights |
| LM Studio | `lm-studio` | `127.0.0.1:1234` | PASS | No key; `~/.lmstudio/models` |
| Phoenix → FinalAI | `phoenix-proxy` | `127.0.0.1:9001` → `50520` | PASS | Health/audit only |
| Modelflare (Cloudflare) | `modelflare.*` settings | Cloudflare AI Gateway | CONFIGURED, PLACEHOLDER | `CLOUDFLARE_ACCOUNT_ID` via env; `modelflare.apiKey` = `PASTE_MODEFLARE_API_KEY_HERE` |
| Tenure | `tenure-local` (agent-hub) | `127.0.0.1:5757` | ENABLED, NO PROVIDERS | `TENURE_API_TOKEN` from `~/.tenure/token` via `.zshenv`; needs onboard provider to expose models |
| OpenAI / Anthropic / Gemini / etc. | `openai`, `anthropic`, `gemini`... | Cloud APIs | DISABLED | `*_API_KEY` env vars needed |

---

## M — Memory / Cache / State

```text
M_model       = model blobs + manifests          (Ollama, LM Studio)
M_runtime     = Redis + workspace/global state   (redis :6379, .con-memory)
M_semantic    = doc index + todo index + memory DB   (orchestrator doc_index.json, todos.json)
M_operational = GAM snapshots + alerts + logs    (drift-memory-guard, .hyperai/logs)
```

| Component | Location | Size | Status | Note |
|-----------|----------|------|--------|------|
| Ollama models | `~/.ollama/models/blobs` | ~18G | PASS | Runtime weights for Ollama |
| LM Studio models | `~/.lmstudio/models` | ~20G | PASS | GGUF/MLX for LM Studio |
| HuggingFace cache | `~/.cache/huggingface/hub` | ~7G | PASS | Dead `gemma-4-26b` partial download removed |
| UV package cache | `~/.cache/uv` | ~1.3G | PASS | Python wheel cache |
| Docker VM | `~/Library/Containers/com.docker.docker/Data/vms` | ~20G | PASS | Container runtime disk |
| Redis runtime state | `127.0.0.1:6379` | — | PASS | Local cache/state |
| Operational logs | `.hyperai/logs` | 1.2G | PASS | Survival governor, orchestrator, escalation logs |
| Disk | `/System/Volumes/Data` | **22G free** | STABLE | Was 100%; Docker prune reclaimed ~13GB |

---

## E — Evidence / Observability / CI

| Component | Artifact | Status | Note |
|-----------|----------|--------|------|
| Unit tests | `tests/test_app.py` | PASS (syntax) | `app.py` compiles; pytest not installed |
| Health probes | `curl` to Ollama, Phoenix, FinalAI, LM Studio, Tenure | PASS | All endpoints responded |
| CI/CD | `.github/workflows/ci-cd.yml` | NOT RUN | Needs push to trigger |
| GAM Memory Guard | `Projects/AI/Tools/ops/drift-memory-guard.sh` | PASS | Executed |
| Mesh probe | `ecosystem_audit/scripts/meshctl.py` | PASS | `probe --write-state` |
| Telemetry router | `HyperAI-Sync/runtime/telemetry_router/scripts/auto_loop.sh` | PASS | Loop active |

---

## Current Operational Verdict

| Layer | Verdict |
|-------|---------|
| A — Authority/Canon | PASS |
| C — VS Code: / Launchd control plane | PASS |
| R — Runtime & bridges | PASS (3 services FAILED due to external dependencies) |
| P — Provider routing | PASS locally; PARTIAL cloud (placeholders) |
| M — Memory/cache/state | PASS (disk STABLE) |
| E — Evidence/CI | PASS locally; NOT RUN remote |
| **Overall** | **OPERATIONAL** |

### Open deltas / failure-cycle watch

1. **Cloud credentials**: Modelflare, OpenAI, Anthropic, Gemini keys are placeholders.
2. **Tenure provider onboard**: `tenure-local` enabled but `/v1/models` returns `[]` until a provider is configured in VS Code:.
3. **External volume**: `registry.dashboard` and `connector.watchdog` need `/Volumes/External/OS_LOGICAL_DEPENDENCY_REGISTRY` mounted.
4. **CloudSync**: Google Drive `rclone` token expired; refresh or reconnect.
5. **CI/CD**: push to run GitHub Actions.
6. **Capacity guard**: disk recovered to 22G free, but historical failure cycle shows degradation will recur without lifecycle budget.

---

## Failure-Cycle History (Canon evidence)

```text
9/5/2026  DEGRADED  → disk full + lineage/entrypoint drift
11/5/2026 PRESSURE  → filesystem saturation spread to shell/IDE/Docker
1/7/2026  PRESSURE  → 639 processes, load avg 54, APFS 97.2%
10/7/2026 GREEN     → Phoenix, FinalAI, Ollama, os.master all healthy
27/7/2026 PRESSURE  → Data volume 100%, HF cache 22G, Ollama blobs 18G
            ↓ cleanup + Docker prune
now       STABLE    → 22G free, core services running
```

**Lesson:** Not a single incident — a recurring failure cycle driven by
`R1` lineage drift, `R2` capacity drift, `R3` control-state fragmentation.
Registry must remain the single source of truth to break the loop.

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
| Google Drive rclone | `rclone config reconnect gdrive:` | token expired |

> **Rule:** Test with placeholders → owner pastes real keys → run end-to-end
> → rotate all exposed keys in one batch before production.
