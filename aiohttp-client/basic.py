import aiohttp
import asyncio
from aiohttp import ClientResponse


async def main():
    resp: ClientResponse

    async with aiohttp.ClientSession() as session:
        async with session.get("http://httpbin.org/get") as resp:

            print(resp.status)
            print(await resp.text())


asyncio.run(main())
