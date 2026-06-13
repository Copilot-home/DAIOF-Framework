#!/usr/bin/env python3
"""OpenAI/Ollama-compatible proxy for Titan FinalAI Chat API.

Runs on the small machine and forwards chat requests to:
  http://192.168.3.158:5052/api/chat/message
"""

from __future__ import annotations

import argparse
import json
import os
import time
import urllib.error
import urllib.request
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from typing import Any


DEFAULT_HOST = "127.0.0.1"
DEFAULT_PORT = 50520
DEFAULT_FINALAI_URL = "http://192.168.3.158:5052/api/chat/message"
DEFAULT_MODEL = "finalai-titan"


def _json_response(handler: BaseHTTPRequestHandler, status: int, payload: dict[str, Any]) -> None:
    body = json.dumps(payload, ensure_ascii=False).encode("utf-8")
    handler.send_response(status)
    handler.send_header("Content-Type", "application/json; charset=utf-8")
    handler.send_header("Content-Length", str(len(body)))
    handler.end_headers()
    handler.wfile.write(body)


def _read_json(handler: BaseHTTPRequestHandler) -> dict[str, Any]:
    length = int(handler.headers.get("Content-Length") or 0)
    raw = handler.rfile.read(length) if length else b"{}"
    if not raw:
        return {}
    return json.loads(raw.decode("utf-8"))


def _messages_to_prompt(messages: list[dict[str, Any]]) -> str:
    chunks: list[str] = []
    for item in messages:
        role = item.get("role", "user")
        content = item.get("content", "")
        if isinstance(content, list):
            parts = []
            for part in content:
                if isinstance(part, dict) and part.get("type") == "text":
                    parts.append(str(part.get("text", "")))
                elif isinstance(part, str):
                    parts.append(part)
            content = "\n".join(parts)
        chunks.append(f"{role}: {content}")
    return "\n\n".join(chunks).strip()


def _call_finalai(url: str, message: str, session_id: str, timeout: int) -> dict[str, Any]:
    payload = json.dumps({"message": message, "session_id": session_id}, ensure_ascii=False).encode("utf-8")
    req = urllib.request.Request(
        url,
        data=payload,
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            raw = resp.read().decode("utf-8")
    except urllib.error.HTTPError as exc:
        raw = exc.read().decode("utf-8", errors="replace")
        try:
            payload = json.loads(raw)
            if isinstance(payload, dict):
                payload.setdefault("http_status", exc.code)
                return payload
        except json.JSONDecodeError:
            pass
        raise RuntimeError(f"FinalAI HTTP {exc.code}: {raw[:500]}") from exc
    except urllib.error.URLError as exc:
        raise RuntimeError(f"FinalAI unreachable: {exc.reason}") from exc
    return json.loads(raw)


class FinalAIProxyHandler(BaseHTTPRequestHandler):
    server_version = "FinalAIOpenAIProxy/1.0"

    def do_GET(self) -> None:  # noqa: N802
        if self.path in {"/health", "/v1/health"}:
            _json_response(self, 200, {"ok": True, "backend": self.server.finalai_url})
            return
        if self.path == "/v1/models":
            now = int(time.time())
            _json_response(
                self,
                200,
                {
                    "object": "list",
                    "data": [
                        {
                            "id": self.server.model_name,
                            "object": "model",
                            "created": now,
                            "owned_by": "titan-finalai",
                        }
                    ],
                },
            )
            return
        if self.path == "/api/version":
            _json_response(self, 200, {"version": "finalai-proxy-1.0"})
            return
        if self.path == "/api/tags":
            now = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
            _json_response(
                self,
                200,
                {
                    "models": [
                        {
                            "name": self.server.model_name,
                            "model": self.server.model_name,
                            "modified_at": now,
                            "size": 0,
                            "digest": "finalai-titan-proxy",
                            "details": {
                                "parent_model": "",
                                "format": "proxy",
                                "family": "finalai",
                                "families": ["finalai"],
                                "parameter_size": "remote",
                                "quantization_level": "remote",
                            },
                        }
                    ]
                },
            )
            return
        _json_response(self, 404, {"error": {"message": "not found", "type": "not_found"}})

    def do_POST(self) -> None:  # noqa: N802
        if self.path == "/api/generate":
            self._handle_ollama_generate()
            return
        if self.path == "/api/chat":
            self._handle_ollama_chat()
            return
        if self.path != "/v1/chat/completions":
            _json_response(self, 404, {"error": {"message": "not found", "type": "not_found"}})
            return

        try:
            request = _read_json(self)
            messages = request.get("messages") or []
            prompt = _messages_to_prompt(messages)
            if not prompt:
                prompt = str(request.get("prompt") or "")
            session_id = str(request.get("user") or request.get("session_id") or "finalai-openai-proxy")
            result = _call_finalai(self.server.finalai_url, prompt, session_id, self.server.backend_timeout)
            content = str(result.get("content") or result.get("message") or result)
            model = str(request.get("model") or self.server.model_name)
            if bool(request.get("stream")):
                self._stream_completion(model, content)
                return
            _json_response(self, 200, self._completion_payload(model, content))
        except Exception as exc:  # FinalAI proxy boundary: expose compact diagnostic to client.
            _json_response(self, 502, {"error": {"message": str(exc), "type": "finalai_proxy_error"}})

    def _handle_ollama_generate(self) -> None:
        try:
            request = _read_json(self)
            prompt = str(request.get("prompt") or "")
            session_id = str(request.get("session_id") or request.get("user") or "finalai-openai-proxy")
            result = _call_finalai(self.server.finalai_url, prompt, session_id, self.server.backend_timeout)
            content = str(result.get("content") or result.get("message") or result)
            payload = {
                "model": str(request.get("model") or self.server.model_name),
                "created_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
                "response": content,
                "done": True,
                "done_reason": "stop",
                "context": [],
                "total_duration": 0,
                "load_duration": 0,
                "prompt_eval_count": 0,
                "prompt_eval_duration": 0,
                "eval_count": 0,
                "eval_duration": 0,
            }
            _json_response(self, 200, payload)
        except Exception as exc:
            _json_response(self, 502, {"error": str(exc)})

    def _handle_ollama_chat(self) -> None:
        try:
            request = _read_json(self)
            prompt = _messages_to_prompt(request.get("messages") or [])
            session_id = str(request.get("session_id") or request.get("user") or "finalai-openai-proxy")
            result = _call_finalai(self.server.finalai_url, prompt, session_id, self.server.backend_timeout)
            content = str(result.get("content") or result.get("message") or result)
            payload = {
                "model": str(request.get("model") or self.server.model_name),
                "created_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
                "message": {"role": "assistant", "content": content},
                "done": True,
                "done_reason": "stop",
                "total_duration": 0,
                "load_duration": 0,
                "prompt_eval_count": 0,
                "prompt_eval_duration": 0,
                "eval_count": 0,
                "eval_duration": 0,
            }
            _json_response(self, 200, payload)
        except Exception as exc:
            _json_response(self, 502, {"error": str(exc)})

    def _completion_payload(self, model: str, content: str) -> dict[str, Any]:
        now = int(time.time())
        return {
            "id": f"chatcmpl-finalai-{now}",
            "object": "chat.completion",
            "created": now,
            "model": model,
            "choices": [
                {
                    "index": 0,
                    "message": {"role": "assistant", "content": content},
                    "finish_reason": "stop",
                }
            ],
            "usage": {
                "prompt_tokens": 0,
                "completion_tokens": 0,
                "total_tokens": 0,
            },
        }

    def _stream_completion(self, model: str, content: str) -> None:
        now = int(time.time())
        self.send_response(200)
        self.send_header("Content-Type", "text/event-stream; charset=utf-8")
        self.send_header("Cache-Control", "no-cache")
        self.send_header("Connection", "close")
        self.end_headers()
        chunk = {
            "id": f"chatcmpl-finalai-{now}",
            "object": "chat.completion.chunk",
            "created": now,
            "model": model,
            "choices": [{"index": 0, "delta": {"content": content}, "finish_reason": None}],
        }
        self.wfile.write(f"data: {json.dumps(chunk, ensure_ascii=False)}\n\n".encode("utf-8"))
        done = {
            "id": f"chatcmpl-finalai-{now}",
            "object": "chat.completion.chunk",
            "created": now,
            "model": model,
            "choices": [{"index": 0, "delta": {}, "finish_reason": "stop"}],
        }
        self.wfile.write(f"data: {json.dumps(done, ensure_ascii=False)}\n\n".encode("utf-8"))
        self.wfile.write(b"data: [DONE]\n\n")
        self.wfile.flush()
        self.close_connection = True

    def log_message(self, fmt: str, *args: Any) -> None:
        if self.server.verbose:
            super().log_message(fmt, *args)


class FinalAIProxyServer(ThreadingHTTPServer):
    finalai_url: str
    model_name: str
    backend_timeout: int
    verbose: bool


def main() -> None:
    parser = argparse.ArgumentParser(description="OpenAI-compatible proxy for Titan FinalAI")
    parser.add_argument("--host", default=os.environ.get("FINALAI_PROXY_HOST", DEFAULT_HOST))
    parser.add_argument("--port", type=int, default=int(os.environ.get("FINALAI_PROXY_PORT", DEFAULT_PORT)))
    parser.add_argument("--backend", default=os.environ.get("FINALAI_BACKEND_URL", DEFAULT_FINALAI_URL))
    parser.add_argument("--model", default=os.environ.get("FINALAI_PROXY_MODEL", DEFAULT_MODEL))
    parser.add_argument("--timeout", type=int, default=int(os.environ.get("FINALAI_BACKEND_TIMEOUT", "120")))
    parser.add_argument("--verbose", action="store_true")
    args = parser.parse_args()

    server = FinalAIProxyServer((args.host, args.port), FinalAIProxyHandler)
    server.finalai_url = args.backend
    server.model_name = args.model
    server.backend_timeout = args.timeout
    server.verbose = args.verbose
    print(f"FinalAI OpenAI proxy listening on http://{args.host}:{args.port}/v1")
    print(f"Forwarding to {args.backend}")
    server.serve_forever()


if __name__ == "__main__":
    main()
