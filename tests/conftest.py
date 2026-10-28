from collections.abc import AsyncIterator

import pytest
from httpx import ASGITransport, AsyncClient

from arbiter.db import engine
from arbiter.main import app
from arbiter.redis import redis_client


@pytest.fixture
async def client() -> AsyncIterator[AsyncClient]:
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        yield ac
    await engine.dispose()
    await redis_client.aclose()

