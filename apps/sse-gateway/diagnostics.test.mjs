import assert from "node:assert/strict";
import test from "node:test";
import { analyzeDeploymentBug } from "./diagnostics.mjs";

test("deployment diagnostics maps auth bottleneck reports to PERFORMANCE branch", () => {
  const output = analyzeDeploymentBug({
    bug_type: "PERFORMANCE",
    environment: "close beta MCP gateway",
    commands: ["curl -N http://localhost:5000/sse?q=email"],
    symptoms: ["auth bottleneck when thousands of MCP services connect"],
    constraints: [{ type: "NO_HACK", value: "no per-service auth workaround" }, { type: "TOPOLOGY_CLEAN" }],
  });

  assert.equal(output.root_cause_branch, "PERFORMANCE");
  assert.equal(output.gate.status, "ACCEPT");
  assert.equal(output.root_cause.layer, "auth-gateway");
  assert.ok(output.verify.steps.some((step) => step.test.includes("POST /auth/exchange")));
});
