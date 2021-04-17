import sys
import functools


@functools.lru_cache(maxsize=1024)
def foo(x):
    return x**2


def test_cached_size():
    max_cached_bytes = sys.getsizeof(job.id) * foo.cache_info().maxsize
    assert max_cached_bytes < 1024 * 1024, "Cache expected < 1MB, reduce maxsize"
