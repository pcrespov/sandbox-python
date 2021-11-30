import pytest


@pytest.fixture(scope="session")
def foo(foo):
    foo_override = foo.copy()
    foo_override["x"] == 42
    return foo_override

def test_it(using_foo):
    print(using_foo)
    assert using_foo["x"] == 42