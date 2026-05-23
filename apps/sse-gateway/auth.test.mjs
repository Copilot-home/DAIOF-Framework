import assert from "node:assert/strict";
import test from "node:test";
import { createAuthService } from "./auth.mjs";

test("gateway tokens verify locally and preserve claims", () => {
  const auth = createAuthService({ authSecret: "test-secret", tokenTtlSeconds: 60 });
  const token = auth.signGatewayToken({ sub: "svc-1", tenant: "close-beta", scope: ["sse:read"] });

  assert.deepEqual(auth.verifyGatewayToken(token).scope, ["sse:read"]);
  assert.equal(auth.verifyGatewayToken(token).sub, "svc-1");
});

test("malformed gateway tokens are rejected without throwing", () => {
  const auth = createAuthService({ authSecret: "test-secret" });

  assert.equal(auth.verifyGatewayToken("gw.not-json.bad-signature"), null);
});

test("short upstream tokens do not authenticate", async () => {
  const auth = createAuthService({ authSecret: "test-secret" });

  assert.equal(await auth.introspectUpstreamToken("short"), null);
});
