import pytest


@pytest.fixture(scope="session")
def foo(foo):
    foo_override = foo.copy()
    foo_override["x"] = 42
    return foo_override

def test_it(using_foo):
    print(using_foo)
    assert using_foo == {"x": 42, "y":3}





def test_of(bar):
    print(bar)
    assert bar ==42

def test_of2(bar):
    print(bar)
    assert bar ==42