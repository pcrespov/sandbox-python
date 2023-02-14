import asyncio

import httpx


async def request(client, n):
    response = await client.get(f"http://172.16.8.55:{8000+n}/get")
    assert response.status_code == 200
    assert response.headers["Connection"] == "keep-alive"


async def request_to_server(client, n):
    await asyncio.gather(*[request(client, n) for _ in range(100)])


async def doit(client):
    await asyncio.gather(*[request_to_server(client, n) for n in range(200)])


async def test_it():
    async with httpx.AsyncClient() as client:
        await asyncio.gather(*[doit(client) for _ in range(500)])

        print(
            "Connections currently in the pull\n",
            len(client._transport._pool.connections),
        )
        print(client._state)
