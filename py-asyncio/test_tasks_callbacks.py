import asyncio
import functools

import pytest

pytestmark = pytest.mark.asyncio


async def succeeds():
    await asyncio.sleep(1)
    return "returned-value"


async def fails():
    print("failing ...")
    await asyncio.sleep(1)
    raise RuntimeError("Failed")

async def fails_fast():
    print("failing ...")
    raise RuntimeError("Failed")

def on_done_log_status(fut: asyncio.Future):
    assert fut.done()

    try:
        # - These two never happen in this context
        # If the Future is done and has a result set by the set_result() method, the result value is returned.
        # If the Future’s result isn’t yet available, this method raises a InvalidStateError exception.

        fut.result()
        # If the Future is done and has an exception set by the set_exception() method, this method raises the exception.
        # If the Future has been cancelled, this method raises a CancelledError exception.
        print("done with success")

    except RuntimeError as err:
        print("done with errors", err)
        # NOTICE that even if not re-raised, the exception is raised if task is awaited!!!
    except asyncio.CancelledError as err:
        print("done with cancellation", err)
        raise # NOTICE that raising or not raising here will not prevent the other on_done callbacks to ru n!!!!

# TESTS -------------

async def test_it():
    tasks = [
        asyncio.create_task(succeeds(), name="1"),
        asyncio.create_task(fails(), name="2"),
        asyncio.create_task(fails_fast(), name="3")
    ]

    tasks_returns = await asyncio.gather(*tasks, return_exceptions=True)
    print(tasks_returns)
    assert any(isinstance(r, RuntimeError) for r in tasks_returns)


    # let's see what happens if I rerun tasks that are done
    assert all(t.done() for t in tasks)
    rerun_tasks_returns = await asyncio.gather(*tasks, return_exceptions=True)

    assert tasks_returns == rerun_tasks_returns


async def test_failing_task():
    task = asyncio.create_task(fails(), name="fails")
    task.add_done_callback(on_done_log_status)

    with pytest.raises(RuntimeError) as exc_info:
        # NOTICE that even if long_task_on_done does not re-raise , 
        # the exception is raised if task is awaited!!!
        await task

    assert exc_info.typename == "RuntimeError" 
    assert exc_info.value.args == ("Failed",)
    # TODO: learn what is https://docs.python.org/3/library/contextvars.html#contextvars.Context


async def test_cancelled_task():
    task = asyncio.create_task(fails(), name="fails")
    task.add_done_callback(functools.partial(print, "\n->First on_done callback for future:"))
    task.add_done_callback(on_done_log_status)
    task.add_done_callback(functools.partial(print, "\n->Second on_done callback for future:"))

    
    task.cancel()
    with pytest.raises(asyncio.CancelledError):
        await task
    
    assert task.cancelled()

    # TODO: learn what is https://docs.python.org/3/library/contextvars.html#contextvars.Context


async def test_scheduled_background_task():

    def _on_done_print_result(future):
        assert future is task
        print(f"got the result and is {future.result()}")

    task = asyncio.create_task(succeeds())
    task.add_done_callback(_on_done_print_result)
    print(task)

    await asyncio.sleep(1)
    print("Hello World!")

    await asyncio.sleep(1)
    print(task)
