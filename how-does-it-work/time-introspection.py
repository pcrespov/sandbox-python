import functools
import time
from functools import lru_cache

N = int(1e9)
print(N)


def stopwatch(func):
    def wrapper(*args, **kwargs):
        tic = time.perf_counter()
        res = func(*args, **kwargs)
        toc = time.perf_counter()
        print(f"{func.__name__}", toc - tic)
        return res

    return wrapper


@lru_cache()
def get_node(id: int) -> int:
    time.sleep(0.1)
    return id


@stopwatch
def introspection():
    results = [n * 2 for n in range(N)]
    assert len(results) == N


@stopwatch
def appending():
    results = []
    for n in range(N):
        results.append(2 * n)
    assert len(results) == N


@stopwatch
def sample_inst():
    result = [get_node(id) for id in range(20) if get_node(id) > 10]
    assert len(result) == 10


@stopwatch
def sample_append():
    result = []
    for id in range(20):
        node = get_node(id)
        if node > 10:
            result.append(node)
    assert len(result) == 10


if __name__ == "__main__":
    appending()
    introspection()
