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


def update_last_visit(session):
    if t := session.get("last_visit"):
        print("Last visit", t)  # time.strftime("%a, %d-%b-%Y %T GMT", t))
    session["last_visit"] = time.time()
    print(session)


async def handler(request):
    session = await get_session(request)
    update_last_visit(session)

    return web.Response(text="OK")


async def one_time_access_handler(request):
    session = await get_session(request)
    update_last_visit(session)
    session["protected_handler"] = True

    return web.Response(text="One time access granted")


async def protected_handler(request):
    session = await get_session(request)
    update_last_visit(session)
    if not session.get("protected_handler"):
        raise web.HTTPUnauthorized
    del session["protected_handler"]

    return web.Response(text="OK")


def init():
    app = web.Application()
    aiohttp_session.setup(
        app,
        EncryptedCookieStorage(
            secret_key=b"Thirty  two  length  bytes  key.",
            cookie_name="sandbox_python.aiolib-session.test_session",
            max_age=1 * _DAY,
            secure=True,
        ),
    )
    app.router.add_route("GET", "/", handler)
    app.router.add_route("GET", "/protected", protected_handler)
    app.router.add_route("GET", "/access", one_time_access_handler)

    return app


@pytest.fixture
def client(event_loop, aiohttp_client) -> TestClient:
    app = init()
    return event_loop.run_until_complete(aiohttp_client(app))


async def test_continuation(client: TestClient):

    response = await client.get("/")
    assert response.status == 200

    response = await client.get("/protected")
    response.cookies
    assert response.status == 401

    # one time access granted
    response = await client.get("/access")
    assert response.status == 200

    response = await client.get("/protected")
    assert response.status == 200
    for _ in range(3):
        response = await client.get("/protected")
        assert response.status == 401


if __name__ == "__main__":
    web.run_app(init())
