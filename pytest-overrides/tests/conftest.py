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