"""Unit tests for HyperAI app.py live runtime."""

import asyncio
import os
from contextlib import asynccontextmanager
from unittest.mock import AsyncMock, MagicMock, patch

import pytest

os.environ.setdefault("LOG_DIR", "/tmp/hyperai_logs")

from app import HyperAIApplication


@pytest.fixture
def app():
    return HyperAIApplication()


def _mock_aiohttp_response(payload=None, status=200):
    """Build an aiohttp-style mock response."""
    response = AsyncMock()
    response.status = status
    response.json = AsyncMock(return_value=payload if payload is not None else {"models": []})
    response.text = AsyncMock(return_value="error")

    @asynccontextmanager
    async def resp_cm():
        yield response

    return resp_cm()


def _mock_aiohttp_session(payload=None, status=200):
    """Build an aiohttp.ClientSession mock whose get() returns an async context manager."""
    session = MagicMock()
    session.get = MagicMock(return_value=_mock_aiohttp_response(payload, status))

    @asynccontextmanager
    async def session_cm():
        yield session

    return session_cm()


def _client_session_factory(payload=None, status=200):
    """Return a MagicMock that, when called, returns an async context manager."""
    return MagicMock(return_value=_mock_aiohttp_session(payload, status))


@pytest.mark.asyncio
async def test_model_list_cache_hits_on_second_call(app):
    """The second call to _list_ollama_models should not hit the network."""
    payload = {"models": [{"name": "qwen2.5:0.5b"}]}
    factory = _client_session_factory(payload)

    with patch("aiohttp.ClientSession", factory):
        r1 = await app._list_ollama_models()
        r2 = await app._list_ollama_models()

    assert r1 == payload
    assert r2 == payload
    assert app._models_cache == payload
    assert factory.call_count == 1


@pytest.mark.asyncio
async def test_model_list_refresh_bypasses_cache(app):
    """refresh=True should always hit the network."""
    first = {"models": [{"name": "qwen2.5:0.5b"}]}
    second = {"models": [{"name": "qwen2.5:0.5b"}, {"name": "llama3"}]}

    call_count = {"value": 0}

    def factory():
        call_count["value"] += 1
        payload = first if call_count["value"] == 1 else second
        return _mock_aiohttp_session(payload)

    with patch("aiohttp.ClientSession", MagicMock(side_effect=factory)):
        r1 = await app._list_ollama_models()
        r2 = await app._list_ollama_models(refresh=True)

    assert r1 == first
    assert r2 == second
    assert call_count["value"] == 2


@pytest.mark.asyncio
async def test_model_list_stale_fallback_when_ollama_unavailable(app):
    """If Ollama is unreachable and we have a cached value, return it marked stale."""
    payload = {"models": [{"name": "qwen2.5:0.5b"}]}

    ok_session = _mock_aiohttp_session(payload)

    @asynccontextmanager
    async def failing_session_cm():
        session = MagicMock()
        session.get = MagicMock(side_effect=RuntimeError("connection refused"))
        yield session

    with patch("aiohttp.ClientSession", MagicMock(return_value=ok_session)):
        r1 = await app._list_ollama_models()

    # Force cache expiry so the next call hits the network and triggers fallback.
    app._models_cache_ts = 0

    with patch("aiohttp.ClientSession", MagicMock(return_value=failing_session_cm())):
        r2 = await app._list_ollama_models()

    assert r2["models"] == payload["models"]
    assert r2.get("stale") is True
    assert "error" in r2


def test_health_check_runs(app):
    """Health check should run without raising and contain expected keys."""
    health = asyncio.run(app.health_check())
    assert health["status"] == "healthy"
    assert "components" in health
    assert set(health["components"].keys()) >= {"hypercore", "ollama", "memory"}
