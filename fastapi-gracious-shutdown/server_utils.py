from functools import wraps


def print_start_and_end(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        print(f"Starting {func.__name__:r} ...")
        try:
            res = await func(*args, **kwargs)
        finally:
            print(f"Completed {func.__name__:r}")
        return res

    return wrapper
