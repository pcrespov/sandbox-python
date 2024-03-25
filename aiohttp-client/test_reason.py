import asyncio
from http import HTTPStatus
from typing import Callable

import pytest
from aiohttp import web
from aiohttp.test_utils import TestClient


@pytest.fixture
def client(
    event_loop: asyncio.AbstractEventLoop,
    aiohttp_client: Callable,
    unused_tcp_port_factory: Callable,
) -> TestClient:

    app = web.Application()

    async def _ok(request):
        raise web.HTTPOk

    async def _error(request):
        raise web.HTTPNotFound

    app.add_routes([web.get("/ok", _ok), web.get("/error", _error)])

    return event_loop.run_until_complete(
        aiohttp_client(app, server_kwargs={"port": unused_tcp_port_factory()})
    )


@pytest.mark.parametrize("path,expected", [("/ok", 200), ("/error", 401)])
async def test_reason_is_automatically_created(
    client: TestClient, path: str, expected: int
):
    response = await client.get(path)

    assert response

    # Elements transmitted in the message and
    #    self.version = message.version
    #    self.status = message.code
    #    self.reason = message.reason

    #    # headers
    #    self._headers = message.headers  # type is CIMultiDictProxy
    #    self._raw_headers = message.raw_headers  # type is Tuple[bytes, bytes]
    assert response.version == (1, 1)
    assert response.status == expected
    assert response.reason == HTTPStatus(response.status).phrase
    # I wonder whether this message is present in the front-end ?
