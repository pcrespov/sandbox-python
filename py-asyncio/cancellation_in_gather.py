#
# Cancelling
#
#

import asyncio
from asyncio.tasks import Task


async def wait(t):
    print("wait", t)
    await asyncio.sleep(t)


async def fail(t):
    print("fail", t)
    await wait(t)
    raise ValueError(f"fail after {t}")


async def killer():
    for t in asyncio.Task.all_tasks():
        if t != asyncio.Task.current_task():
            print("killing", t)
            t.cancel()


async def echo_forever(t):
    while True:
        print("*")
        await asyncio.sleep(t)


async def gather_and_wait(coros):
    try:
        res = await asyncio.gather(*coros)
        print(res)
    except asyncio.CancelledError as err:
        print("Cancelled", err)


def fire_and_forget(coros):
    asyncio.ensure_future(asyncio.gather(*coros))


async def run():
    # await gather_and_wait([wait(1), wait(2), fail(1)])
    fire_and_forget([wait(1), wait(2), fail(1), echo_forever(1)])


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(run())
