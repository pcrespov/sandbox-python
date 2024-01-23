# pylint: disable=redefined-outer-name
# pylint: disable=unused-argument
# pylint: disable=unused-variable
# pylint: disable=too-many-arguments

import aiohttp_session
import pytest
from aiohttp import web
from aiohttp.test_utils import TestClient
from aiohttp_session import AbstractStorage, SimpleCookieStorage, get_session
from aiohttp_session.cookie_storage import EncryptedCookieStorage

_MIN = 60  # secs
_HOUR = 60 * _MIN  # secs
_DAY = 24 * _HOUR  # sec


@pytest.fixture
def cookie_name():
    return "AIOHTTP_SESSION_FOO"


@pytest.fixture(params=["secure", "simple"])
def storage(request: pytest.FixtureRequest, cookie_name: str) -> AbstractStorage:

    if request.param == "secure":
        return EncryptedCookieStorage(
            secret_key=b"Thirty  two  length  bytes  key.",
            cookie_name=cookie_name,
            max_age=5 * _DAY,
            # secure=True, WARNING:this is only for HTTPS! the TestClient deletes the cookie on every call with this option
        )
    elif request.param == "simple":
        return SimpleCookieStorage(cookie_name=cookie_name)


async def _get_session_handler(request):
    session = await get_session(request)
    user_name, product_name = session["my_session"]
    return web.json_response([user_name, product_name])


async def _create_session_handler(request):
    session = await get_session(request)
    session["my_session"] = ["my-user-name", "my-product-name"]

    return web.Response(text="OK")


@pytest.fixture
def client(
    event_loop, aiohttp_client, storage: AbstractStorage, cookie_name: str
) -> TestClient:

    # app
    app = web.Application()
    app.router.add_route("GET", "/session", _get_session_handler)
    app.router.add_route("POST", "/session", _create_session_handler)
    aiohttp_session.setup(app, storage)

    return event_loop.run_until_complete(aiohttp_client(app))


async def test_it(client: TestClient, cookie_name: str):

    response = await client.post("/session")
    assert response.ok

    print(response.cookies[cookie_name].value)
    # >> response.cookies["AIOHTTP_SESSION"].value
    #   '{"created": 1706031544, "session": {"my_session": ["username", "productname"]}}'

    response = await client.get("/session")
    assert response.ok
    got = await response.json()
    assert got == ["my-user-name", "my-product-name"]
