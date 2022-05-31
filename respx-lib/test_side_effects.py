import pytest
from faker import Faker
from respx import MockRouter
import respx
import httpx


#
# https://lundberg.github.io/respx/guide/#mock-with-a-side-effect
#


@pytest.fixture
def mocked_service_api(faker: Faker):

    with respx.mock(  # type: ignore
        base_url="http://service:8080/v0",
        assert_all_called=True,
        assert_all_mocked=True,
    ) as respx_mock:
        # /ping
        respx_mock.get(path="/ping", name="ping")

        # /echo
        def echo(req: httpx.Request):
            print(req.content.decode(req.headers.encoding))
            return httpx.Response(200, content=req.content)

        respx_mock.post(path="/echo").mock(side_effect=echo)

        yield respx_mock


def test_it(mocked_service_api: MockRouter):

    with httpx.Client(base_url="http://service:8080/v0") as client:
        resp = client.get("/ping")
        assert resp.status_code == 200
        assert mocked_service_api["ping"].called

        data = {"x": 42}
        resp = client.post("/echo", json=data)
        assert resp.status_code == 200
        assert resp.json() == data
