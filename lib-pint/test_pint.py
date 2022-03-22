# https://pint.readthedocs.io/en/stable/

import math

import pytest
from pint import Quantity, Unit, UnitRegistry, set_application_registry


@pytest.fixture
def ureg():
    return UnitRegistry()


def test_it(ureg: UnitRegistry):

    q = 3 * ureg.meter + 4 * ureg.cm
    print(q)

    assert isinstance(q, Quantity)
    assert isinstance(q.units, Unit)

    print(q.magnitude)
    print(q.units)
    print(q.dimensionality)

    d = 3.4 * ureg.kilometres

    assert isinstance(d, Quantity)
    print(d.magnitude)
    print(d.units)
    print(d.dimensionality)

    assert d.to("meter").magnitude == 3400.0


def test_converter(ureg: UnitRegistry):
    Q_ = ureg.Quantity

    t = Q_("0 * kelvin").to("degree_Celsius")
    print(t)

    a = Q_("45 * degrees").to("radians")
    print(a)

    s = Q_("1 km/hour**0.5").to("mm/sec**0.5")

    print("{:~P}".format(s))

    print(f"{s:P}")  # pretty
    print(f"{s:~P}")  # short pretty
    print(f"{s:~L}")  # latex
    print(f"{s:~H}")  # htl format
    print(f"{s:H}")  # htl format


def test_wrappers(ureg: UnitRegistry):

    # https://pint.readthedocs.io/en/stable/wrapping.html

    @ureg.wraps(None, ("meter", "meter"))
    def g(x, y):
        return (x - y) / (x + y) * math.log2(x / y)
