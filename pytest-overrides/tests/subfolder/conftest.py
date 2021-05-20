
import pytest

@pytest.fixture
def username(username):
    return 'overridden-' + username