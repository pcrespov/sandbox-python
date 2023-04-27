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
        assert_all_called=True,
        assert_all_mocked=True,
    ) as respx_mock:

        respx_mock.get(path="/ping", name="ping").respond(status_code=204)

        # /projects
        respx_mock.post(
            path__regex=r"/projects$",
            name="create_project",
        ).respond(json={"created": True})

        respx_mock.get(
            path__regex=r"/projects/(?P<project_id>\d+)/nodes/(?P<node_id>\d+)",
            name="get_project",
        ).respond(json={"project_id": faker.uuid4()})

        yield respx_mock


def test_path(mocked_service_api: MockRouter):

    with httpx.Client(base_url="http://director-v2:8000/v2") as client:

        resp = client.get("/ping")
        assert resp.status_code == 204
        assert mocked_service_api["ping"].called

        resp = client.get("/projects/123/nodes/123")
        assert resp.status_code == 200
        assert mocked_service_api["get_project"].called

        resp = client.post("/projects", params={"hidden": True}, json={"create": True})

        assert (
            f"{resp.request.url}" == "http://director-v2:8000/v2/projects?hidden=true"
        )
        assert resp.status_code == 200
        assert resp.json()["created"] == True
        assert mocked_service_api["create_project"].called
