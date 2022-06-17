from functools import wraps
from typing import Callable
import time
import inspect
import asyncio

# Emulator
async def emulate(raise_error: bool, delay: int, orphan_task: str):
    if raise_error:
        raise RuntimeError()

    if delay:
        await asyncio.sleep(delay)

    if orphan_task:

        async def run_forever():
            while True:
                await asyncio.sleep(1)

        asyncio.create_task(run_forever(), name=orphan_task)


def log_fun(log: Callable):
    def decorator(function):
        assert inspect.iscoroutinefunction(function)

        func_name = f"{function.__name__!r}"

        @wraps(function)
        async def wrapper(*args, **kwargs):
            tic = time.perf_counter()
            log(f"{func_name} started ...")
            try:
                returned = await function(*args, **kwargs)
            finally:
                elapsed = time.perf_counter() - tic
                log(f"{func_name} done [{elapsed=:3.2f}s]")
            return returned

        return wrapper

    return decorator
