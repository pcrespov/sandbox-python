import pytest


def foo(x, y):
    return x+y


def _foo(x, y):
    return x

@pytest.fixture
def foo_patched(mocker):


    m = mocker.patch("test_sideeffects.foo", return_value=42, autospec=True)
    return m


def test_it(foo_patched):

    assert foo(3,2) == 42
    assert foo_patched == foo
    assert foo_patched.call_count == 1
    assert foo.call_args.args == (3,2)

    foo_patched.side_effect = _foo
    assert foo(3,4) == 3


