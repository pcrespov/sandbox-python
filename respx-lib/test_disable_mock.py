# pylint: disable=redefined-outer-name
# pylint: disable=unused-argument
# pylint: disable=unused-variable
# pylint: disable=too-many-arguments

from typing import Iterator

import httpx
import pytest
import respx
from faker import Faker
from respx import MockRouter


@pytest.fixture
def mocked_service_api(faker: Faker, use_real_api: bool) -> Iterator[MockRouter]:

    with respx.mock(  # type: ignore
        base_url="https://httpbin.org/",
        assert_all_called=False,
        assert_all_mocked=True,
    ) as respx_mock:

        respx_mock.get(path="/get", name="get").respond(status_code=204, json={"x": 42})

        # SEE https://github.com/lundberg/respx/issues/95#issuecomment-721061582
        if use_real_api:
            respx_mock.stop()
        yield respx_mock


@pytest.mark.parametrize("use_real_api", [False])
def test_against_mocked_api(mocked_service_api: MockRouter):
    with httpx.Client(base_url="https://httpbin.org/") as client:
        resp = client.get("/get")

        assert resp.status_code == 204
        assert resp.json() == {"x": 42}
        assert mocked_service_api["get"].called


@pytest.mark.parametrize("use_real_api", [True])
def test_against_real_api(mocked_service_api: MockRouter):

    with httpx.Client(base_url="https://httpbin.org/") as client:
        resp = client.get("/get")

        assert resp.status_code == 200
        assert resp.json() != {"x": 42}
        assert "get" not in mocked_service_api
