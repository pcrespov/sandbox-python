import pytest

@pytest.fixture()
def some_fixture():
    print("started")
    yield 3
    print("cleanup")


@pytest.mark.parametrize("p", (1, 2, 3))
def test_it(p, some_fixture):
    print("param", p, some_fixture)
    assert p