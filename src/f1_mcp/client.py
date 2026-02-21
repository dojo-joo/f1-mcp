"""Async HTTP client for the OpenF1 API."""

import os
from typing import Any

import httpx

BASE_URL = "https://api.openf1.org/v1"
_TOKEN = os.environ.get("OPENF1_API_TOKEN")

# Shared async client (created per-request context via dependency injection or
# used as a module-level singleton in async contexts).
_client: httpx.AsyncClient | None = None


def _make_client() -> httpx.AsyncClient:
    headers = {"Accept": "application/json"}
    if _TOKEN:
        headers["Authorization"] = f"Bearer {_TOKEN}"
    return httpx.AsyncClient(
        base_url=BASE_URL,
        headers=headers,
        timeout=15.0,
    )


async def get_client() -> httpx.AsyncClient:
    global _client
    if _client is None or _client.is_closed:
        _client = _make_client()
    return _client


def _strip_none(params: dict[str, Any]) -> dict[str, Any]:
    return {k: v for k, v in params.items() if v is not None}


async def fetch(endpoint: str, params: dict[str, Any] | None = None) -> list[dict]:
    """GET an OpenF1 endpoint and return the JSON list."""
    client = await get_client()
    clean = _strip_none(params or {})
    response = await client.get(f"/{endpoint}", params=clean)
    response.raise_for_status()
    return response.json()


async def fetch_latest_session_key() -> int | None:
    """Return the session_key of the most recent session."""
    data = await fetch("sessions", {"order_by": "-date_start", "limit": 1})
    if data:
        return data[0].get("session_key")
    return None
