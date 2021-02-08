# https://www.python-httpx.org/async/#streaming-responses
# 


import httpx

import asyncio

import aiofiles

async def main():
    async with httpx.AsyncClient() as client:
        async with client.stream('GET', "http://127.0.0.1:8000/redirect") as resp:
            async with aiofiles.open('filename', mode="wb") as fh:
                async for chunk in resp.aiter_bytes():
                    print(len(chunk))
                    await fh.write(chunk)
                    print(".")




asyncio.run(main())