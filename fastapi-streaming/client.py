# https://www.python-httpx.org/async/#streaming-responses
#
import sys
import httpx
import asyncio
import aiofiles
import aiodocker


async def main():
    endpoint = "redirect"
    if len(sys.argv) > 1:
        endpoint = sys.argv[1]

    async with httpx.AsyncClient() as client:
        async with client.stream("GET", f"http://127.0.0.1:8000/{endpoint}") as resp:
            async with aiofiles.open("filename", mode="wb") as fh:
                async for chunk in resp.aiter_bytes():
                    print(len(chunk))
                    await fh.write(chunk)
                    print(".")


asyncio.run(main())
