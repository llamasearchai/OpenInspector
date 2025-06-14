import json
import pytest
from httpx import AsyncClient

from openinspector.api import app


@pytest.mark.asyncio
async def test_health():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        resp = await ac.get("/health")
        assert resp.status_code == 200
        assert resp.json() == {"status": "ok"}


@pytest.mark.asyncio
async def test_signal_ingest():
    payload = {"type": "authentication", "user_id": "test", "success": False}
    async with AsyncClient(app=app, base_url="http://test") as ac:
        resp = await ac.post("/signals", json=payload)
        assert resp.status_code == 200
        data = resp.json()
        assert data["detection"] is not None 