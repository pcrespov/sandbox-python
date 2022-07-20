import asyncio
from contextlib import suppress


async def coro(delay):
    await asyncio.sleep(delay)
    return delay


async def coro_blocking(delay):
    with suppress(asyncio.CancelledError):
        return await coro(delay)
    return await coro(delay)

async def main():

    r = await asyncio.wait_for(coro(1), timeout=3)
    print(r)

    try:
        await asyncio.wait_for(coro(3), timeout=1)
    except asyncio.TimeoutError as err:
        print(err)


    for c in (coro, coro_blocking):
        print(c)
        t = asyncio.create_task(c(5))
        t.cancel()
        try:
            await asyncio.wait_for(t, timeout=1)
        except asyncio.CancelledError as err:
            print(err)
        except asyncio.TimeoutError as err:
            print(err)


asyncio.run(main())
