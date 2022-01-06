import asyncio
from contextlib import AbstractAsyncContextManager, asynccontextmanager


@asynccontextmanager
async def lock_context():
    print("before context 1")
    yield
    print("after context 1")


lock = asyncio.Lock()


@asynccontextmanager
async def acquire_context():

        try:
            async with lock:
                print("acquiring context")

            yield
            print("releasing context")

        except ValueError:
            print("something went wrong")
            raise

    print("after context1 is finished")


async def run_task():
    print("init")
    async with acquire_context():
        print("running task")
    print("done")


asyncio.run(asyncio.gather())
