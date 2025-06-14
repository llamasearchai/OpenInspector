from __future__ import annotations

import httpx
from typing import Any, Dict

from .config import settings


class OpenInspectorClient:
    """Convenience client for publishing signals to an OpenInspector server."""

    def __init__(self, base_url: str | None = None, timeout: float = 10.0):
        self.base_url = base_url or f"http://{settings.api_host}:{settings.api_port}"
        self._client = httpx.Client(timeout=timeout)

    def send_signal(self, **signal: Any) -> Dict[str, Any]:
        """Send a signal payload and return the server response."""
        resp = self._client.post(f"{self.base_url}/signals", json=signal)
        resp.raise_for_status()
        return resp.json()

    def health(self) -> bool:
        try:
            resp = self._client.get(f"{self.base_url}/health")
            return resp.status_code == 200
        except httpx.HTTPError:
            return False

    def close(self):
        self._client.close()

    # allow usage with context manager
    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc, tb):
        self.close() 