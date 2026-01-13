"""
uv run --with aiohttp --with pytest-asyncio pytest test_aiohttp_with_pytest_asyncio.py

OR

uv venv
source .venv/bin/activate
uv pip sync requirements-dev.txt
pytest test_aiohttp_with_pytest_asyncio.py
"""

import pytest
from aiohttp import web
from aiohttp.test_utils import TestClient

pytest_plugins = [
    "aiohttp.pytest_plugin",  # No need to install pytest-aiohttp separately
]


# Example taken from https://docs.aiohttp.org/en/stable/testing.html
async def hello(request):
    return web.Response(text="Hello, world")


@pytest.fixture
async def client(aiohttp_client):
    app = web.Application()
    app.router.add_get("/", hello)
    return await aiohttp_client(app)


async def test_hello(client: TestClient):
    resp = await client.get("/")
    assert resp.status == 200
    text = await resp.text()
    assert "Hello, world" in text
