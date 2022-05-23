
from email.mime import base
from typing import Iterator

import httpx
import pytest
import respx
from faker import Faker
from respx import MockRouter


@pytest.fixture
def mocked_service_api(faker: Faker) -> Iterator[MockRouter]:

     with respx.mock(  # type: ignore
        base_url="http://service:8080/v0",
        assert_all_called=True,
        assert_all_mocked=True,
    ) as respx_mock:

        respx_mock.get(path="/ping", name="ping")

        # TODO: Not sure what are the regex keys for
        respx_mock.get(path__regex=r"/projects/(?P<project_id>\d+)/nodes/(?P<node_id>\d+)", name="get_project").respond(json={"project_id": faker.uuid4()})
        yield respx_mock




def test_path( mocked_service_api: MockRouter):

    with httpx.Client(base_url="http://service:8080/v0") as client:

        resp = client.get("/ping")
        assert resp.status_code == 200
        assert mocked_service_api["ping"].called

        resp = client.get("/projects/123/nodes/123")
        assert resp.status_code == 200
        assert mocked_service_api["get_project"].called


