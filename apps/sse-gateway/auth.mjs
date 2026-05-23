import crypto from "node:crypto";

const DEFAULT_AUTH_SECRET = "close-beta-dev-secret";
const DEFAULT_TOKEN_TTL_SECONDS = 300;
const DEFAULT_INTROSPECTION_CACHE_SECONDS = 60;

export function createAuthService(options = {}) {
  const authSecret = options.authSecret || process.env.AUTH_SECRET || DEFAULT_AUTH_SECRET;
  const tokenTtlSeconds = Number(options.tokenTtlSeconds || process.env.TOKEN_TTL_SECONDS) || DEFAULT_TOKEN_TTL_SECONDS;
  const introspectionCacheSeconds =
    Number(options.introspectionCacheSeconds || process.env.INTROSPECTION_CACHE_SECONDS) ||
    DEFAULT_INTROSPECTION_CACHE_SECONDS;

  const tokenCache = new Map();
  const inflightIntrospection = new Map();

  function signGatewayToken(claims, ttlSeconds = tokenTtlSeconds) {
    const now = Math.floor(Date.now() / 1000);
    const payload = {
      ...claims,
      iat: now,
      exp: now + ttlSeconds,
      iss: "sse-gateway",
    };

    const body = base64url(JSON.stringify(payload));
    const sig = base64url(crypto.createHmac("sha256", authSecret).update(body).digest());
    return `gw.${body}.${sig}`;
  }

  function verifyGatewayToken(token) {
    if (!token?.startsWith("gw.")) return null;

    const parts = token.split(".");
    if (parts.length !== 3) return null;
    const [, body, providedSig] = parts;

    const expectedSig = base64url(crypto.createHmac("sha256", authSecret).update(body).digest());
    const a = Buffer.from(providedSig);
    const b = Buffer.from(expectedSig);
    if (a.length !== b.length || !crypto.timingSafeEqual(a, b)) return null;

    const payload = parseGatewayPayload(body);
    if (!payload) return null;

    const now = Math.floor(Date.now() / 1000);
    if (!payload.exp || payload.exp < now) return null;

    return payload;
  }

  async function introspectUpstreamToken(token) {
    if (inflightIntrospection.has(token)) return inflightIntrospection.get(token);

    const p = (async () => {
      const now = Math.floor(Date.now() / 1000);
      const cached = tokenCache.get(token);
      if (cached && cached.exp > now) return cached.claims;

      // Placeholder for external IdP introspection. In close beta we only accept long-enough tokens.
      if (token.length < 16) return null;

      const claims = {
        sub: crypto.createHash("sha1").update(token).digest("hex").slice(0, 12),
        tenant: "close-beta",
        scope: ["mcp:connect", "sse:read"],
      };

      tokenCache.set(token, { claims, exp: now + introspectionCacheSeconds });
      return claims;
    })();

    inflightIntrospection.set(token, p);
    try {
      return await p;
    } finally {
      inflightIntrospection.delete(token);
    }
  }

  async function authenticateRequest(req) {
    const token = extractBearerToken(req);
    if (!token) return null;

    const gwClaims = verifyGatewayToken(token);
    if (gwClaims) return gwClaims;

    const upstreamClaims = await introspectUpstreamToken(token);
    if (!upstreamClaims) return null;

    return {
      ...upstreamClaims,
      via: "upstream-introspection",
    };
  }

  return {
    authenticateRequest,
    signGatewayToken,
    verifyGatewayToken,
    introspectUpstreamToken,
    tokenTtlSeconds,
  };
}

export function extractBearerToken(req) {
  const raw = req.headers.authorization || "";
  return raw.startsWith("Bearer ") ? raw.slice(7).trim() : "";
}

export function hasScope(claims, scope) {
  return Array.isArray(claims?.scope) && claims.scope.includes(scope);
}

function base64url(input) {
  return Buffer.from(input)
    .toString("base64")
    .replace(/=/g, "")
    .replace(/\+/g, "-")
    .replace(/\//g, "_");
}

function parseGatewayPayload(body) {
  try {
    return JSON.parse(fromBase64url(body).toString("utf8"));
  } catch {
    return null;
  }
}

function fromBase64url(input) {
  const normalized = input.replace(/-/g, "+").replace(/_/g, "/");
  const padded = normalized.padEnd(normalized.length + ((4 - (normalized.length % 4)) % 4), "=");
  return Buffer.from(padded, "base64");
}
