
import pytest


@pytest.fixture(scope="session")
def foo():
    return {"x": 33}


@pytest.fixture(scope="module")
def using_foo(foo):
    bar = foo.copy()
    bar.update(y=3)
    return bar