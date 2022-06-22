import asyncio

import async_timeout
import httpx

## https://github.com/ITISFoundation/osparc-simcore/pull/3129

GG_TEST_URL = "https://www.google.com"
MS_TEST_URL = "https://www.microsoft.com"

timeout = httpx.Timeout(3.0, connect=5.0, pool=1.0)
limits = httpx.Limits(max_connections=5)



async def get_url_with_async_timeout(client, url):
    # This is not cancelling tasks
    try:
        async with async_timeout.timeout(delay=0.1):
            return await client.get(url)
    except asyncio.TimeoutError:
        print(f"calling {url} timed-out")
        return "timed-out"


async def get_url_with_asyncio(client, url):
    # this is cancelling tasks
    try:
        return await asyncio.wait_for(client.get(url), timeout=0.1)
    except asyncio.TimeoutError:
        print(f"calling {url} timed-out")
        return "timed-out"


async def test():
    async with httpx.AsyncClient(timeout=timeout, limits=limits) as client:
        tasks = {
            asyncio.create_task(get_url_with_asyncio(client, GG_TEST_URL))
            for _ in range(10)
        } | {
            asyncio.create_task(get_url_with_asyncio(client, MS_TEST_URL))
            for _ in range(10)
        }

        # Wait for first one to terminate.
        done, pending = await asyncio.wait(tasks, return_when=asyncio.FIRST_COMPLETED)
        print(client._transport._pool.connections)

        await asyncio.wait(tasks, return_when=asyncio.ALL_COMPLETED)
        print(client._transport._pool.connections)

        for task in tasks:
            assert task.done()
            response = task.result()
            if isinstance(response, httpx.Response):
                print(f"response from {response.url}", response.status_code)
            else:
                print(f"reponse is {response}")

        wiki_response = await client.get("https://www.wikipedia.com") # works nicely with asyncio, badly with async-timeout
        print(f"response from {wiki_response.url}", wiki_response.status_code)


if __name__ == "__main__":
    asyncio.run(test())
