# SSE Gateway (functional stream)

## Why this auth model scales for close beta

Instead of calling a central auth server for every `/sse` connection, this gateway supports:

1. **Token exchange** (`POST /auth/exchange`): validate upstream bearer once, issue short-lived gateway token.
2. **Local verification** (`GET /sse`): verify gateway token locally with HMAC (no network hop).
3. **Single-flight + cache** for upstream introspection to avoid auth stampedes.
4. **Structured diagnostics** (`POST /diagnostics`): map PR/issue symptoms into the deployment diagnostic schema (`diagnostic-contract.schema.json`) so the right team can own the fix.

This reduces auth bottlenecks when thousands of MCP services connect concurrently and gives close-beta incidents a consistent handoff format.

## Run

```bash
node apps/sse-gateway/server.mjs
```

Set `AUTH_SECRET` before any shared or public deployment:

```bash
AUTH_SECRET="replace-with-a-rotated-secret" node apps/sse-gateway/server.mjs
```

## Get gateway token (close beta pattern)

```bash
curl -s -X POST \
  -H "Authorization: Bearer upstream_token_1234567890" \
  http://localhost:5000/auth/exchange
```

## Connect SSE using gateway token

```bash
curl -N \
  -H "Authorization: Bearer <gatewayToken>" \
  "http://localhost:5000/sse?q=email"
```

You should receive:
- `status` event
- `result` event
- periodic keep-alive comments (`: keep-alive`)

## Map a real PR/issue into the diagnostic contract

```bash
curl -s -X POST \
  -H "Content-Type: application/json" \
  http://localhost:5000/diagnostics \
  -d '{
    "input": {
      "bug_type": "PERFORMANCE",
      "environment": "close beta MCP gateway",
      "commands": ["curl -N http://localhost:5000/sse?q=email"],
      "symptoms": ["auth bottleneck when thousands of MCP services connect"],
      "constraints": [
        { "type": "NO_HACK", "value": "no per-service auth workaround" },
        { "type": "TOPOLOGY_CLEAN" }
      ]
    }
  }'
```

Use the `output.root_cause_branch` field to route work:

| Branch | Owner direction | Practical action |
| --- | --- | --- |
| `PERFORMANCE` | Gateway/Auth team | Measure auth exchange p95, cache hit ratio, and SSE connection count. |
| `STRUCTURAL` | Platform/Topology team | Fix schema, route, namespace, and deployment topology before code patches. |
| `RUNTIME` | App Runtime team | Reproduce with commands, logs, status codes, and SSE frame capture. |
| `SILENT` | Observability team | Add logs/metrics/traces before changing behavior. |

## Test

```bash
npm test
```
