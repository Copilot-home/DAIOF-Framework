# Ecosystem Relationship Report (Upstream/Downstream, Deep Review)

## Scope đã rà soát
- Repo topology và chuẩn tài liệu nội bộ.
- Connector mesh + integration APIs.
- Runtime stacks: Python, Node, Docker.
- VSCode host/extension ecosystem (local merged source snapshot).
- GitHub ecosystem (API + repository automation intent).

## Nguyên tắc mô hình hóa
**Đơn vị nhỏ nhất = dependency (depen) = node.**

Mỗi node có thể là:
1. Library/package dependency.
2. Service endpoint/API dependency.
3. Runtime container/service dependency.
4. Connector contract dependency.
5. Dev-tool dependency (VSCode extension/toolchain).

## Node inventory (high-level)

### A) Runtime Dependency Nodes
- Python deps: `numpy`, `PyGithub`, `pyyaml`, `pathlib2`, `requests`.
- Node deps: `express`, `@playwright/test`.
- Container base deps:
  - `python:3.11-slim` (runtime image),
  - `node:lts-alpine` (gateway image).

### B) Integration/API Nodes
- GitHub API (`https://api.github.com`) qua connector `github`.
- Jira API (`https://your-jira-domain.atlassian.net`) qua connector `jira`.
- Asana API (`https://app.asana.com/api/1.0`) qua connector `asana`.
- Linear API (`https://api.linear.app`) qua connector `linear`.
- SMTP server qua connector `mail`.
- Telegram Bot API qua connector `telegram`.
- LLM providers: OpenAI key + local Ollama endpoint.

### C) Coordination Mesh Nodes
- `conductor` (orchestrator)
- `mcp_hub` (subscribe/claim/release protocol)
- `runtime_observer` (presence/heartbeat)
- `llm_engine` (analysis/generation)
- `web_agent` (web recon/search/scrape)
- `tech_debt_auditor` (periodic debt scan)

### D) Interface & Ecosystem Nodes
- SSE Gateway (`apps/sse-gateway/server.mjs`) cho stream events.
- VSCode merged extension tree (`vscode-merged/extensions/*`) như upstream mirror/vendor surface trong workspace.
- GH repository automation surface qua workflow/docs references trong README.

## Upstream / Downstream map

### Upstream (nguồn phụ thuộc đi vào hệ)
1. Package registries (PyPI/NPM).
2. Container registries (Docker Hub base images).
3. External SaaS APIs (GitHub/Jira/Asana/Linear/Telegram/SMTP/OpenAI).
4. VSCode extension upstream sources (được mirror trong `vscode-merged`).

### Core Processing Mesh
`conductor -> mcp_hub -> runtime_observer -> domain connectors -> notification channels`

### Downstream (đầu ra hệ)
1. Queue mailboxes giữa connectors.
2. SSE stream output cho client/host integration.
3. Metrics/health artifacts và logs.
4. Issue/PR/workflow actions sang GitHub/issue trackers.

## Findings quan trọng sau rà soát sâu
1. **Tài liệu kiến trúc đang đa lớp nhưng thiếu một bản đồ node-edge chuẩn hóa liên repo.**
2. **Connector schema đã khá đồng bộ, nhưng chuẩn “upstream/downstream contract” chưa được formalize thành artifact machine-readable.**
3. **SSE gateway có dấu hiệu conflict code path (trùng khai báo `PORT`, mixed http+express flow) cần chuẩn hóa để làm host extension bridge ổn định.**
4. **Cloud/API migration đã có phase docs, nhưng chưa có bảng dependency risk theo từng external API node.**

## Chuẩn hóa tài liệu đề xuất (cross-repo)

### 1) Chuẩn artifact bắt buộc cho mỗi repo trong ecosystem
- `docs/operations/ECOSYSTEM_NODE_MAP.yaml` (node/edge machine-readable).
- `docs/operations/UPSTREAM_DOWNSTREAM_CONTRACT.md` (human-readable contract).
- `docs/operations/DEPENDENCY_RISK_REGISTER.md` (security/availability/legal risk by node).

### 2) Chuẩn taxonomy node thống nhất toàn hệ
- `dep.library`
- `dep.service_api`
- `dep.container_base`
- `dep.connector`
- `dep.devtool`
- `dep.data_store`

### 3) Chuẩn scorecard cho mỗi node
- `criticality` (low/medium/high)
- `blast_radius`
- `rotation_strategy`
- `fallback_mode`
- `owner`
- `slo/sla`

## Kế hoạch đóng vòng kỹ thuật (đề xuất thực thi)

### Phase 1 — Inventory & Contract Freeze
- Xuất full node map từ dependencies + connectors + runtime services.
- Chốt upstream/downstream contract cho host extension, gh api, cloud ai endpoints.

### Phase 2 — Hardening & Fault Campaign
- Chạy fault/chaos simulation theo node class.
- Thu attack/error vectors vào risk register theo node.

### Phase 3 — Migration Readiness
- Đánh dấu node nào sẽ bị thay thế khi API/protocol mới ra mắt.
- Thiết lập compatibility adapters có sunset date.

## Kết luận
Hệ đã có nền orchestration tốt. Để “flow scale” và vận hành ecosystem thực sự bền, cần xem dependency như node chuẩn hóa ngay từ tài liệu + contract machine-readable, sau đó mới tối ưu hóa runtime và migration API mới một cách có kiểm soát.
