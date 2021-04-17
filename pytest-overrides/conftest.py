
import pytest


@pytest.fixture(scope="session")
def foo():
    return {"x": 33}


@pytest.fixture(scope="module")
def using_foo(foo):
    bar = foo.copy()
    bar.update(y=3)
    return bar


@pytest.fixture(scope="module")
def bar():
    print("bar")
    return 1


@pytest.fixture(scope="session")
def bar(bar):
    print("override and expand scope to session")
    print("session with bar")
    return  42 + bar