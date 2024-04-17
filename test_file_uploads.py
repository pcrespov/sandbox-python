# pylint: disable=redefined-outer-name
# pylint: disable=unused-argument
# pylint: disable=unused-variable
# pylint: disable=too-many-arguments


from pathlib import Path
from typing import Annotated, AsyncIterator

import httpx
import pytest
from asgi_lifespan import LifespanManager
from fastapi import FastAPI, File, UploadFile
from httpx import ASGITransport

MAX_TIME_FOR_APP_TO_STARTUP = 10
MAX_TIME_FOR_APP_TO_SHUTDOWN = 10


@pytest.fixture
def file_path(tmp_path: Path):
    p = tmp_path / "foo.txt"
    p.write_text("foo")
    return p


@pytest.fixture
def app_fixture(file_path: Path):
    app = FastAPI()

    @app.put("/upload")
    async def upload(file: Annotated[UploadFile, File(...)]):
        assert file.filename == file_path.name
        assert file.file.read() == file_path.read_bytes()

    return app


@pytest.fixture
async def client(
    app_fixture: FastAPI,
) -> AsyncIterator[httpx.AsyncClient]:
    async with LifespanManager(
        app_fixture,
        startup_timeout=None,
        shutdown_timeout=None,
    ), httpx.AsyncClient(
        base_url="http://api.testserver.io",
        headers={
            "Content-Type": "application/json"
        },  # <-- this is a problem for file parameters!
        transport=ASGITransport(app=app_fixture),
    ) as httpx_async_client:
        yield httpx_async_client


async def test_it(client: httpx.AsyncClient, file_path: Path):
    client.headers.pop("Content-Type")
    with file_path.open("rb") as fh:
        resp = await client.put(
            "/upload",
            files={"file": fh},
            headers={},
        )
    resp.raise_for_status()
