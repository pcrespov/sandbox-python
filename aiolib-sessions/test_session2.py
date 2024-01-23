import time

import aiohttp_session
import pytest
from aiohttp import web
from aiohttp.test_utils import TestClient
from aiohttp_session import get_session
from aiohttp_session.cookie_storage import EncryptedCookieStorage

_MIN = 60  # secs
_HOUR = 60 * _MIN  # secs
_DAY = 24 * _HOUR  # sec



async def get_session_handler(request):
    session = await get_session(request)
    data = session["my_session"]
    return web.json_response(data)

async def create_session_handler(request):
    session = await get_session(request)
    session["my_session"] = ("username", "productname")

    return web.Response(text="OK")



def init():
    app = web.Application()
    aiohttp_session.setup(
        app,
        EncryptedCookieStorage(
            secret_key=b"Thirty  two  length  bytes  key.",
            cookie_name="sandbox_python.aiolib-session.test_session",
            # max_age=1 * _DAY,
            # secure=True, WARNING: the TestClient deletes the cookie on every call with this option
        ),
    )
    app.router.add_route("GET", "/session", get_session_handler)
    app.router.add_route("POST", "/session", create_session_handler)
    
    return app


# --------------------------------------------------------------------------------------------------------------


@pytest.fixture
def client(event_loop, aiohttp_client) -> TestClient:
    app = init()
    return event_loop.run_until_complete(aiohttp_client(app))


async def test_it(client: TestClient):

    response = await client.post("/session")
    assert response.ok

    response = await client.get("/session")
    assert response.ok
    got = await response.json()
    assert got == ["username", "productname"]
        


# if __name__ == "__main__":
#     web.run_app(init())
