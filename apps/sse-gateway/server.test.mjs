import assert from "node:assert/strict";
import test from "node:test";
import { createGatewayServer } from "./server.mjs";

async function withServer(run) {
  const server = createGatewayServer({ auth: { authSecret: "test-secret", tokenTtlSeconds: 60 } });
  await new Promise((resolve) => server.listen(0, "127.0.0.1", resolve));
  const { port } = server.address();

  try {
    await run(`http://127.0.0.1:${port}`);
  } finally {
    await new Promise((resolve) => server.close(resolve));
  }
}

test("auth exchange returns a gateway token", async () => {
  await withServer(async (baseUrl) => {
    const response = await fetch(`${baseUrl}/auth/exchange`, {
      method: "POST",
      headers: { Authorization: "Bearer upstream_token_1234567890" },
    });
    const body = await response.json();

    assert.equal(response.status, 200);
    assert.equal(body.ok, true);
    assert.match(body.gatewayToken, /^gw\./);
  });
});

test("SSE requires a valid token and streams status/result frames", async () => {
  await withServer(async (baseUrl) => {
    const exchange = await fetch(`${baseUrl}/auth/exchange`, {
      method: "POST",
      headers: { Authorization: "Bearer upstream_token_1234567890" },
    });
    const { gatewayToken } = await exchange.json();

    const controller = new AbortController();
    const response = await fetch(`${baseUrl}/sse?q=email`, {
      headers: { Authorization: `Bearer ${gatewayToken}` },
      signal: controller.signal,
    });
    const reader = response.body.getReader();
    const decoder = new TextDecoder();
    let output = "";

    while (!output.includes("event: result")) {
      const { value } = await reader.read();
      output += decoder.decode(value);
    }
    controller.abort();

    assert.equal(response.status, 200);
    assert.match(response.headers.get("content-type"), /text\/event-stream/);
    assert.match(output, /event: status/);
    assert.match(output, /data: \{"query":"email","intent":"email","tools":\["Gmail"\]\}/);
  });
});

test("diagnostics endpoint returns schema-shaped output", async () => {
  await withServer(async (baseUrl) => {
    const response = await fetch(`${baseUrl}/diagnostics`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        input: {
          bug_type: "STRUCTURAL",
          environment: "close beta",
          commands: ["npm run sse:gateway"],
          symptoms: ["schema handoff missing"],
          constraints: [{ type: "DATA_FIRST" }],
        },
      }),
    });
    const body = await response.json();

    assert.equal(response.status, 200);
    assert.equal(body.ok, true);
    assert.equal(body.output.root_cause_branch, "STRUCTURAL");
    assert.equal(body.output.gate.status, "ACCEPT");
  });
});
