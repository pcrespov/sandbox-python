import asyncio

import pytest

pytestmark = pytest.mark.asyncio


async def foo():
    await asyncio.sleep(1)
    return "Foo!"


async def fails():
    print("failing ...")
    await asyncio.sleep(1)
    raise RuntimeError("Failed")


def long_task_on_done(fut: asyncio.Future):
    assert fut.done()

    try:
        # - These two never happen in this context
        # If the Future is done and has a result set by the set_result() method, the result value is returned.
        # If the Future’s result isn’t yet available, this method raises a InvalidStateError exception.

        fut.result()
        # If the Future is done and has an exception set by the set_exception() method, this method raises the exception.
        # If the Future has been cancelled, this method raises a CancelledError exception.

    except RuntimeWarning as err:
        print("done with errors", err)
    except asyncio.CancelledError as err:
        print("cancelled", err)
        raise


async def hello_world():
    task = asyncio.create_task(foo())

    def got_result(future):
        assert future is task
        print(f"got the result! {future.result()}")

    task.add_done_callback(got_result)
    print(task)
    await asyncio.sleep(1)
    print("Hello World!")
    await asyncio.sleep(1)
    print(task)


async def test_it():
    task = asyncio.create_task(fails(), name="fails")
    task.add_done_callback(long_task_on_done)

    with pytest.raises(RuntimeError) as exc_info:
        await task

    # TODO: learn what is https://docs.python.org/3/library/contextvars.html#contextvars.Context


def test_basic():
    asyncio.run(hello_world())
