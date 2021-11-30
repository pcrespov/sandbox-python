import asyncio

import aiohttp
import pytest
from aiohttp import web


@pytest.fixture(scope="session")
async def global_data():
    await asyncio.sleep(0.1)
    return 42


@pytest.fixture(scope="module")
async def module_data():
    await asyncio.sleep(0.1)
    return 42


@pytest.fixture()
async def func_data(loop):
    await asyncio.sleep(0.1)
    return 42


async def hello(request):
    return web.Response(text="Hello, world")


async def test_hello(aiohttp_client, loop):
    app = web.Application()
    app.router.add_get("/", hello)
    client = await aiohttp_client(app)
    resp = await client.get("/")
    assert resp.status == 200
    text = await resp.text()
    assert "Hello, world" in text


async def test_me(global_data, module_data, func_data):
    assert global_data == module_data
    assert func_data == module_data
