"""Tests for using aiohttp with pytest-asyncio."""

# USAGE
"""
uv run --with aiohttp --with pytest-asyncio pytest test_aiohttp_with_pytest_asyncio.py

OR

uv venv
source .venv/bin/activate
uv pip install -r requirements-dev.txt
pytest test_aiohttp_with_pytest_asyncio.py
"""

import asyncio
import pytest

from aiohttp import web
from aiohttp.test_utils import TestClient

pytest_plugins = [
    "aiohttp.pytest_plugin",  # No need to install pytest-aiohttp separately
]


@pytest.fixture
async def loop() -> asyncio.AbstractEventLoop:
    """Override the event loop inside `aiohttp.pytest_plugin` with the one from `pytest-asyncio`.

    This provides the necessary fixtures to use pytest-asyncio with aiohttp!!!

    USAGE:

        pytest_plugins = [
            "aiohttp.pytest_plugin",  # No need to install pytest-aiohttp separately
        ]


    ERRORS:
        Otherwise error like this will be raised:

        >        if connector._loop is not loop:
        >           raise RuntimeError("Session and connector has to use same event loop")
        E           RuntimeError: Session and connector has to use same event loop

        .venv/lib/python3.11/site-packages/aiohttp/client.py:375: RuntimeError

        >        if connector._loop is not loop:
        >           raise RuntimeError("Session and connector has to use same event loop")
        >E           RuntimeError: Session and connector has to use same event loop

        .venv/lib/python3.11/site-packages/aiohttp/client.py:375: RuntimeError
    """
    return asyncio.get_running_loop()


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
