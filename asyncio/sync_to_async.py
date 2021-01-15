import asyncio
import time
from asyncio.exceptions import CancelledError


def run_async_as_sync(coro):
    loop = asyncio.get_event_loop()
    loop.run_until_complete(coro)


async def the_async_fun():
    print("the_async_fun")
    await asyncio.sleep(1)


async def some_background_task():
    try:
        while True:
            print(".", flush=True)
            await asyncio.sleep(0.5)
    except Exception:
        import pdb

        pdb.set_trace()
        print("x")


async def setup_background_task():
    task = asyncio.create_task(some_background_task(), name="background task")
    try:
        await asyncio.wait_for(task, timeout=3)
    except asyncio.TimeoutError:
        pass


if __name__ == "__main__":
    print("main")
    
    # run_async_as_sync(the_async_fun())
    run_async_as_sync(setup_background_task())

    # block
    for n in range(3):
        print("o")
        time.sleep(1)

    print("done")
