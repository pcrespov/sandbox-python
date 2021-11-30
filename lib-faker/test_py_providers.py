# https://faker.readthedocs.io/en/master/providers/faker.providers.python.html

from faker import Faker
import pytest

Faker.seed(0)
_fake = Faker()


@pytest.mark.parametrize(
    "value", (_fake.pyint(min_value=0, max_value=10, step=2) for _ in range(5))
)
def test_as_param(value: int):
    assert isinstance(value, int)
    assert value < 10


def test_fixture_factory(faker: Faker):
    assert faker.pyfloat(positive=True) > 0
