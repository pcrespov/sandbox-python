# TODO: 
# 
# - Can you override fixtures of different scopes?
#
#
# https://docs.pytest.org/en/stable/fixture.html#overriding-fixtures-on-various-levels
import pytest

@pytest.fixture
def username():
    return 'username'

@pytest.fixture
def other_username(username):
    return 'other-' + username


@pytest.fixture(scope="session")
def foo():
    return {"x": 33}


@pytest.fixture(scope="module")
def using_foo(foo):
    bar = foo.copy()
    bar.update(y=3)
    return bar