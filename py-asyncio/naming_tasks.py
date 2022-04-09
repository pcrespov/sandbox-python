## https://docs.python.org/3/library/asyncio-task.html#sleeping

import asyncio
import time


async def say_after(delay, what):
    await asyncio.sleep(delay)
    print(what)


async def main():
    task1 = asyncio.create_task(say_after(1, "hoi"), name="bar")

    task2 = asyncio.create_task(say_after(2, "zaeme"), name="bar")

    print(f"started at {time.strftime('%X')}")

    # Wait until both tasks are completed (should take
    # around 2 seconds.)
    await task1
    await task2

    print(f"finished at {time.strftime('%X')}")


asyncio.run(main())
