# pylint: disable=redefined-outer-name
# pylint: disable=unused-argument
# pylint: disable=unused-variable
# pylint: disable=too-many-arguments

from contextlib import asynccontextmanager
from typing import AsyncIterator, TypedDict

import pytest
from fastapi import FastAPI, PlainTextResponse, Request
from starlette.testclient import TestClient

#
# https://www.starlette.io/lifespan/
#


@pytest.fixture
def app():
    class State(TypedDict):
        name: str

    @asynccontextmanager
    async def lifespan(app: FastAPI) -> AsyncIterator[State]:
        print(
            "start: Starlette will not start serving any incoming requests until the lifespan has been run."
        )

        # Consider using https://anyio.readthedocs.io/en/stable/tasks.html for managing async tasks
        yield {"name": "foo"}

        print(
            "teardown: The lifespan teardown will run once all connections have been closed, and any in-process background tasks have completed"
        )

    the_app = FastAPI(lifespan=lifespan)

    @the_app.get("/")
    async def homepage(request: Request):
        name = request.state.name
        return PlainTextResponse(f"request state was {name}")


def test_homepage(app: FastAPI):
    with TestClient(app) as client:
        # Application's lifespan is called on entering the block.
        response = client.get("/")
        assert response.status_code == 200

    # And the lifespan's teardown is run when exiting the block.
