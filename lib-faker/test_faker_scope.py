import pytest
from faker import Faker

#
# in .venv/lib/python3.8/site-packages/faker/contrib/pytest/plugin.py
#
# we can see that faker has scope=function !!!
# should not be used otherwise

#
# pytest -v -s --setup-show test_faker_scope.py
#


# @pytest.fixture(scope="module")
# def faker_seed():
# TODO: Not clear to me how does this seed affects
#     return 3


@pytest.fixture()
def one(faker: Faker):
    return faker.pyint()


@pytest.fixture
def two(faker: Faker):
    return faker.pyint()


def test_it(one, two):
    print()
    print("-" * 100)
    print(f"{one=}, {two=}")
    print("-" * 100)

    assert one != two


def test_also(one, two):
    print()
    print("-" * 100)
    print(f"{one=}, {two=}")
    print("-" * 100)

    assert one != two
