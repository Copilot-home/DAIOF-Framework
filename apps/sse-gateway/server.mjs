import http from "node:http";
import { pathToFileURL } from "node:url";
import { createAuthService, hasScope } from "./auth.mjs";
import { analyzeDeploymentBug } from "./diagnostics.mjs";

const PORT = Number(process.env.PORT) || 5000;
const MAX_JSON_BODY_BYTES = Number(process.env.MAX_JSON_BODY_BYTES) || 64 * 1024;

function detectIntent(q = "") {
  const s = String(q).toLowerCase();

  if (s.includes("email")) return ["email", ["Gmail"]];
  if (s.includes("docs")) return ["docs", ["Google Docs"]];
  if (s.includes("storage")) return ["storage", ["Google Drive"]];
  if (s.includes("dev")) return ["dev", ["Replit", "Vercel"]];
  if (s.includes("payment")) return ["payment", ["PayPal"]];
  if (s.includes("ai")) return ["ai", ["Hugging Face"]];

  return ["general", ["General"]];
}

function writeSseEvent(res, event, data) {
  res.write(`event: ${event}\n`);
  res.write(`data: ${JSON.stringify(data)}\n\n`);
}

function writeJson(res, status, payload) {
  res.writeHead(status, { "Content-Type": "application/json; charset=utf-8" });
  res.end(JSON.stringify(payload));
}

function readJsonBody(req) {
  return new Promise((resolve, reject) => {
    let body = "";

    req.setEncoding("utf8");
    req.on("data", (chunk) => {
      body += chunk;
      if (Buffer.byteLength(body, "utf8") > MAX_JSON_BODY_BYTES) {
        reject(new Error("JSON body exceeds limit"));
        req.destroy();
      }
    });
    req.on("end", () => {
      if (!body.trim()) {
        resolve({});
        return;
      }

      try {
        resolve(JSON.parse(body));
      } catch {
        reject(new Error("Invalid JSON body"));
      }
    });
    req.on("error", reject);
  });
}

export function createGatewayServer(options = {}) {
  const auth = options.authService || createAuthService(options.auth || {});

  return http.createServer(async (req, res) => {
    const url = new URL(req.url || "/", `http://${req.headers.host || "localhost"}`);

    if (req.method === "GET" && url.pathname === "/") {
      writeJson(res, 200, { ok: true, service: "sse-gateway" });
      return;
    }

    if (req.method === "POST" && url.pathname === "/auth/exchange") {
      const claims = await auth.authenticateRequest(req);
      if (!claims) {
        writeJson(res, 401, { ok: false, error: "Unauthorized" });
        return;
      }

      const gatewayToken = auth.signGatewayToken({
        sub: claims.sub,
        tenant: claims.tenant || "close-beta",
        scope: claims.scope || ["sse:read"],
      });

      writeJson(res, 200, { ok: true, gatewayToken, expiresIn: auth.tokenTtlSeconds });
      return;
    }

    if (req.method === "POST" && url.pathname === "/diagnostics") {
      try {
        const body = await readJsonBody(req);
        writeJson(res, 200, { ok: true, output: analyzeDeploymentBug(body.input || body) });
      } catch (error) {
        writeJson(res, 400, { ok: false, error: error.message });
      }
      return;
    }

    if (req.method === "GET" && url.pathname === "/sse") {
      const claims = await auth.authenticateRequest(req);
      if (!claims || !hasScope(claims, "sse:read")) {
        writeJson(res, 401, { ok: false, error: "Unauthorized" });
        return;
      }

      const q = String(url.searchParams.get("q") || "");
      const [intent, tools] = detectIntent(q);

      res.writeHead(200, {
        "Content-Type": "text/event-stream; charset=utf-8",
        "Cache-Control": "no-cache",
        Connection: "keep-alive",
      });

      writeSseEvent(res, "status", { status: "processing", sub: claims.sub });

      const resultTimer = setTimeout(() => {
        writeSseEvent(res, "result", { query: q, intent, tools });
      }, 300);

      const heartbeat = setInterval(() => {
        res.write(": keep-alive\n\n");
      }, 15000);

      req.on("close", () => {
        clearTimeout(resultTimer);
        clearInterval(heartbeat);
        res.end();
      });
      return;
    }

    writeJson(res, 404, { ok: false, error: "Not found" });
  });
}

if (import.meta.url === pathToFileURL(process.argv[1]).href) {
  createGatewayServer().listen(PORT, "0.0.0.0", () => {
    console.log(`SSE server running on ${PORT}`);
  });
}
