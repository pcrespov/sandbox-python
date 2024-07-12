import asyncio
import concurrent
import time

import toolz

# REFERENCES
# - https://docs.python.org/3/library/asyncio-eventloop.html#id14
#


async def to_async_in_loop(blocking_io, *args):
    # 1. Run in the default loop's executor:
    return await asyncio.get_running_loop().run_in_executor(
        None,
        blocking_io,
        *args,
    )


async def to_async_in_thread_pool(blocking_io, *args):
    # 2. Run in a custom thread pool:
    with concurrent.futures.ThreadPoolExecutor() as pool:
        return await asyncio.get_running_loop().run_in_executor(
            pool,
            blocking_io,
            *args,
        )


async def to_async_in_process_pool(cpu_bound, *args):
    # 3. Run in a custom process pool:
    with concurrent.futures.ProcessPoolExecutor() as pool:
        return await asyncio.get_running_loop().run_in_executor(
            pool,
            cpu_bound,
            *args,
        )


# examples
def fun_blocking_io(x):
    # File operations (such as logging) can block the
    # event loop: run them in a thread pool.
    with open("/dev/urandom", "rb") as f:
        return f.read(100)
    return x


def fun_cpu_bound(x):
    # CPU-bound operations will block the event loop:
    # in general it is preferable to run them in a
    # process pool.
    sum(i * i for i in range(10**7))
    return x


_run_fun = fun_cpu_bound
_to_async = to_async_in_loop


def _run_partition(chunk):
    # emulates validation of a
    return list(map(_run_fun, chunk))


def sync_run(data, partition_size):
    if partition_size < 2:
        return list(_run_fun(_) for _ in data)

    return list(
        toolz.concat(
            _run_partition(chunk) for chunk in toolz.partition_all(partition_size, data)
        )
    )


async def async_run(data, partition_size):
    if partition_size < 2:
        return await asyncio.gather(*(_to_async(_run_fun, _) for _ in data))

    return list(
        toolz.concat(
            await asyncio.gather(
                *(
                    _to_async(_run_partition, chunk)
                    for chunk in toolz.partition_all(partition_size, data)
                ),
                return_exceptions=True,
            )
        )
    )


if __name__ == "__main__":

    title = str((_run_fun.__name__, _to_async.__name__))

    print(f"{title:-^100}")
    N = 50
    data = list(range(N))
    print(f"{len(data)=}")

    expected = list(data)
    partition_size = 1

    print("- async_run", f"{partition_size=}")
    t0 = time.time()
    got = asyncio.run(async_run(data, partition_size))
    print(time.time() - t0)

    # Sync
    print("- sync_run", f"{partition_size=}")
    t0 = time.time()
    sync_run(data, partition_size)
    print(time.time() - t0)

    assert got == expected
    expected = list(got)
