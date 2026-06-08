import http from "node:http";

const PORT = Number(process.env.PORT) || 5000;

import express from "express";

const app = express();
const PORT = Number(process.env.PORT) || 5000;

app.get("/", (_req, res) => {
  res.json({ ok: true, service: "sse-gateway" });
});

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

const server = http.createServer((req, res) => {
  const url = new URL(req.url || "/", `http://${req.headers.host || "localhost"}`);

  if (req.method === "GET" && url.pathname === "/") {
    res.writeHead(200, { "Content-Type": "application/json; charset=utf-8" });
    res.end(JSON.stringify({ ok: true, service: "sse-gateway" }));
    return;
  }

  if (req.method === "GET" && url.pathname === "/sse") {
    const q = String(url.searchParams.get("q") || "");
    const [intent, tools] = detectIntent(q);

    res.writeHead(200, {
      "Content-Type": "text/event-stream; charset=utf-8",
      "Cache-Control": "no-cache",
      Connection: "keep-alive",
    });

    writeSseEvent(res, "status", { status: "processing" });

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

  res.writeHead(404, { "Content-Type": "application/json; charset=utf-8" });
  res.end(JSON.stringify({ ok: false, error: "Not found" }));
});

server.listen(PORT, "0.0.0.0", () => {
app.get("/sse", (req, res) => {
  const q = String(req.query.q || "");
  const [intent, tools] = detectIntent(q);

  res.setHeader("Content-Type", "text/event-stream; charset=utf-8");
  res.setHeader("Cache-Control", "no-cache");
  res.setHeader("Connection", "keep-alive");

  if (typeof res.flushHeaders === "function") {
    res.flushHeaders();
  }

  res.write("event: status\n");
  res.write(`data: ${JSON.stringify({ status: "processing" })}\n\n`);

  const resultTimer = setTimeout(() => {
    res.write("event: result\n");
    res.write(
      `data: ${JSON.stringify({
        query: q,
        intent,
        tools,
      })}\n\n`,
    );
  }, 300);

  const heartbeat = setInterval(() => {
    res.write(": keep-alive\n\n");
  }, 15000);

  req.on("close", () => {
    clearTimeout(resultTimer);
    clearInterval(heartbeat);
    res.end();
  });
});

app.listen(PORT, "0.0.0.0", () => {
  console.log(`SSE server running on ${PORT}`);
});
