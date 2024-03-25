import asyncio
import inspect
from http import HTTPStatus
from typing import Callable

import aiohttp.web_exceptions
import pytest
from aiohttp import web
from aiohttp.test_utils import TestClient


def is_http_exception_with_status(obj):
    """Predicate function to check if an object is a subclass of HttpException with a valid status_code."""
    return (
        inspect.isclass(obj)
        and issubclass(obj, aiohttp.web_exceptions.HTTPException)
        and hasattr(obj, "status_code")
        and obj.status_code != -1
        and (obj.status_code < 300 or obj.status_code >= 400)  # avoids redirections
    )


http_exception_cls_map = {
    cls.status_code: cls
    for _, cls in inspect.getmembers(
        aiohttp.web_exceptions, is_http_exception_with_status
    )
}


def _get_http_response(request: web.Request, code: int):
    http_exception_cls = http_exception_cls_map[code]
    match code:
        case 300 | 301 | 302 | 303 | 305 | 307 | 308:
            http_response = http_exception_cls(
                location="https://httpbin.org/"
            )  # headers["Location"]
            # for 3XX the problem is that it redirects and the response is the redirection
        case web.HTTPMethodNotAllowed.status_code:
            http_response = web.HTTPMethodNotAllowed(
                method=request.method, allowed_methods=["FOO"]
            )  # header["Allow"] = "POST,GET"
        case web.HTTPRequestEntityTooLarge.status_code:
            http_response = web.HTTPRequestEntityTooLarge(
                max_size=10, actual_size=23
            )  # text
        case web.HTTPUnavailableForLegalReasons.status_code:
            http_response = web.HTTPUnavailableForLegalReasons(
                link="https://httpbin.org/"
            )  # headers["Link"]
        case _:
            http_response = http_exception_cls()
    return http_response


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

    async def _raise(request: web.Request):
        code = int(request.query["code"])
        http_response = _get_http_response(request, code)
        raise http_response

    async def _return(request: web.Request):
        code = int(request.query["code"])
        http_response = _get_http_response(request, code)
        raise http_response

    app.add_routes(
        [
            web.get("/ok", _ok),
            web.get("/error", _error),
            web.post("/raise", _raise),
            web.post("/return", _return),
        ]
    )

    return event_loop.run_until_complete(
        aiohttp_client(app, server_kwargs={"port": unused_tcp_port_factory()})
    )


@pytest.mark.parametrize("path,expected_status_code", [("/ok", 200), ("/error", 404)])
async def test_reason_is_automatically_created(
    client: TestClient, path: str, expected_status_code: int
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
    assert response.content_type == "text/plain"
    assert response.version == (1, 1)
    assert response.status == expected_status_code
    assert response.reason == HTTPStatus(response.status).phrase
    # check the default
    assert await response.text() == f"{response.status}: {response.reason}"
    # I wonder whether this message is present in the front-end ?

    response = await client.post(path)
    assert response.status == web.HTTPMethodNotAllowed.status_code
    assert response.headers["Allow"] == "GET,HEAD"


@pytest.mark.parametrize("path", ("/raise", "/return"))
@pytest.mark.parametrize("code", http_exception_cls_map)
async def test_raise_http_responses(client: TestClient, path: str, code: int):
    response = await client.post(path, params={"code": code})

    assert response.status == code
    assert response.reason == HTTPStatus(response.status).phrase

    text = await response.text()
    if response.content_length:
        assert not http_exception_cls_map[code].empty_body
        assert text

        assert response.content_type == "text/plain"
        if code != web.HTTPRequestEntityTooLarge.status_code:  # 413
            assert text == f"{response.status}: {response.reason}"
    else:
        assert http_exception_cls_map[code].empty_body
        assert not text
