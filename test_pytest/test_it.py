from contextlib import contextmanager

import pytest


@contextmanager
def context_42():
    print("in")
    yield 42
    print("out")


@pytest.fixture
def foo():
    with context_42() as value:
        yield value


def test_it2(foo):
    assert foo == 42
