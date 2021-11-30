import asyncio

import aiohttp
import pytest
from aiohttp import web


@pytest.fixture(scope="session")
def session_loop():
    # will create if does not exists
    return asyncio.get_event_loop()


@pytest.fixture(scope="session")
async def global_data(session_loop: asyncio.AbstractEventLoop):
    print(f"{session_loop=}", id(session_loop))
    assert asyncio.get_running_loop() == session_loop

    assert asyncio.current_task(session_loop) is not None

    print("Number of tasks in session_loop", len(asyncio.all_tasks(session_loop)))

    await asyncio.sleep(0.1)
    yield 42

    assert asyncio.get_running_loop() == session_loop

    # ...


# @pytest.fixture(scope="module")
# async def module_data():
#     await asyncio.sleep(0.1)
#     return 42


@pytest.fixture()
async def func_data(loop: asyncio.AbstractEventLoop):
    print(f"{loop=}", id(loop))
    assert asyncio.get_running_loop() == loop

    assert asyncio.current_task(loop) is not None

    print("Number of tasks in loop", len(asyncio.all_tasks(loop)))

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


async def test_me(global_data, func_data):
    assert global_data == func_data
