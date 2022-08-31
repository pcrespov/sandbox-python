#
#

#

import asyncio
from inspect import isawaitable
import random
from typing import Any, Callable

import pytest

pytestmark = pytest.mark.asyncio


async def fail(v=0):
    print("fails", v)
    d = 1 + random.random()
    await asyncio.sleep(d)
    raise ValueError(f"failed {v} after {d}")


async def succeed(v=0):
    print("succeds", v)
    await asyncio.sleep(1 + random.random())
    return v


async def go(v):
    coro = random.choice([fail, succeed])
    return await coro(v)


#################################


async def assert_all_cancelled(exclude=[]):
    exclude_ = [
        asyncio.current_task(),
    ] + exclude
    await asyncio.sleep(0)
    for t in asyncio.all_tasks():
        if t not in exclude_:
            assert t.done() or t.cancelled()


####
async def safe_gather(*coros_or_futures, loop=None, return_exceptions=False):
    tasks = [
        c if asyncio.isfuture(c) else asyncio.create_task(c) for c in coros_or_futures
    ]

    try:
        return await asyncio.gather(
            *tasks, loop=loop, return_exceptions=return_exceptions
        )

    except Exception:
        # children are removed
        for t in tasks:
            t.cancel()
        raise


#########################


async def run_worker(queue: asyncio.Queue, func: Callable, results: list[Any]):
    while True:
        try:
            arg = await queue.get()
            # Remove and return an item from the queue. If queue is empty, wait until an item is available.
            result = await func(arg)
            results.append(result)
        finally:
            # https://docs.python.org/3/library/asyncio-queue.html#asyncio.Queue.task_done
            # Used by queue consumers. For each get() used to fetch a task, a subsequent
            # call to task_done() tells the queue that the processing on the task is complete.
            queue.task_done()


async def run_w_workers():
    #
    # SEE https://www.pythonfixing.com/2022/01/fixed-how-to-asynciogather-tasks-in.html
    #

    max_workers = 50

    queue = asyncio.Queue(max_workers)
    results = []
    workers = [
        asyncio.create_task(run_worker(queue, succeed, results))
        for i in range(max_workers)
    ]

    try:
        for value in range(1000):
            await queue.put(value)
        # TODO: if something fails, raise right away and delete the rest

        await queue.join()

    finally:

        for w in workers:
            assert not w.exception()

        for w in workers:
            w.cancel()

    return results


#
# TESTS ---------------------------
#


async def test_run_w_workers():
    await run_w_workers()

    for t in asyncio.all_tasks():
        if t not in asyncio.current_task():
            assert t.done() or t.cancelled()


async def test_run():
    coros = [succeed() for _ in range(10000)]
    r = await safe_gather(coros)
    assert r == list(range(10000))

    for t in asyncio.all_tasks():
        if t not in asyncio.current_task():
            assert t.done() or t.cancelled()

    coros = [succeed() for _ in range(10000)] + [fail() for _ in range(5)]
    with pytest.raises(ValueError):
        await safe_gather(coros)

    for t in asyncio.all_tasks():
        if t not in asyncio.current_task():
            assert t.done() or t.cancelled()


pytest.main(["-x", __file__])
