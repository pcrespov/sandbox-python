import httpx
import aiofiles
import aiofiles.os
from pathlib import Path

import asyncio


def about_timeout():
    timeout = httpx.Timeout(5, read=11)
    with httpx.Client(timeout=timeout) as client:
        r = client.get("http://127.0.0.1:8000/delay")


async def download_and_save_file(output_path: Path):
    async def _download_chunk(client: httpx.AsyncClient):
        url =  "http://127.0.0.1:8000/large-file"
        async with client.stream("GET", url) as resp:
            print(resp.headers)
            if int(resp.headers["Content-Length"]) < 1024 * 1024:
                print("direct download")
                chunk = await resp.aread()
                yield chunk

            print("downloading by chunk")
            async for chunk in resp.aiter_bytes():
                yield chunk

    output_path.resolve().parent.mkdir(parents=True, exist_ok=True)

    async with httpx.AsyncClient(timeout=httpx.Timeout(5.0, read=3600)) as client:
        async with aiofiles.open(output_path, mode="wb") as fh:
            file_size = 0
            async for chunk in _download_chunk(client):
                if chunk:
                    print("saving chunk", len(chunk), "bytes")
                    await fh.write(chunk)
                    file_size += len(chunk)
            print("Saved", file_size, "bytes")
        print(await aiofiles.os.stat(output_path))


if __name__ == "__main__":
    # about_timeout()
    asyncio.run(download_and_save_file(Path("ignore/downloaded.txt")))
