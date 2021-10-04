import pytest


MOCKED_RETURNED = 0


@pytest.fixture
def mock_foo(mocker):
    mocks = {}

    for func in ("mylib.api.foo", "mylib.core.foo"):
        mocks[func] = mocker.patch(func, return_value=MOCKED_RETURNED)
    return mocks


def test_api(mock_foo):

    from mylib.api import foo

    assert foo(1) == MOCKED_RETURNED

    assert mock_foo["mylib.api.foo"].called
    assert not mock_foo["mylib.core.foo"].called



def test_core(mock_foo):

    from mylib.core import foo

    assert foo(1) == MOCKED_RETURNED

    assert not mock_foo["mylib.api.foo"].called
    assert mock_foo["mylib.core.foo"].called


def test_bar(mock_foo):

    from mylib.bar import bar

    assert bar(1) == MOCKED_RETURNED + 42

    # NOTE: bar imports foo via api!!
    assert mock_foo["mylib.api.foo"].called
    assert not mock_foo["mylib.core.foo"].called


