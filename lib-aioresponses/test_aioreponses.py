import pytest
from aiohttp import ClientSession
from aioresponses import aioresponses

# LIMITATION: see https://github.com/pnuckowski/aioresponses/issues/230


@pytest.fixture
def mock_aioresponse():
    with aioresponses() as m:
        m.get("http://example.com/foo", status=200)
        yield m


async def test_with_full_url(mock_aioresponse: aioresponses):
    async with ClientSession() as session:
        async with session.get("http://example.com/foo") as response:
            assert response.ok


async def test_with_relative_url(mock_aioresponse: aioresponses):
    async with ClientSession(base_url="http://example.com") as session:
        async with session.get("/foo") as response:
            assert response.ok
