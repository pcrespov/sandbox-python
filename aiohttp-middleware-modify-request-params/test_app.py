
from main import app
from aiohttp.test_utils import TestClient

def client(loop, aiohttp_client):
    return loop.run_until_complete(aiohttp_client(app))

async def test_it(client: TestClient):

    await client.get("/prj/1")
    await client.get("/prj/2")
