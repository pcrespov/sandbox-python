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
def mocked_service_api(faker: Faker) -> Iterator[MockRouter]:

    with respx.mock(  # type: ignore
        base_url="http://director-v2:8000/v2",
        assert_all_called=False,
        assert_all_mocked=True,
    ) as respx_mock:

        respx_mock.get(path="/get", name="get").respond(status_code=204)

        yield respx_mock


def test_it(mocked_service_api: MockRouter):
    with httpx.Client(base_url="http://director-v2:8000/v2") as client:
        resp = client.get("/get")

        assert resp.status_code == 204

        assert mocked_service_api["get"].called


def test_it2(mocked_service_api: MockRouter):
    mocked_service_api.route(pass_through=True)

    with httpx.Client(base_url="https://httpbin.org/") as client:
        resp = client.get("/get")

        assert resp.status_code == 200
        assert not mocked_service_api["get"].called
