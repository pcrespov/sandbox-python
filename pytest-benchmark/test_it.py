## https://pytest-benchmark.readthedocs.io/

import pytest
import itertools
from collections import namedtuple

from dataclasses import dataclass


@dataclass
class ServiceOutput:
    label: str


ServiceInput = ServiceOutput
UnitRegistry = int

fake_outputs = [ServiceOutput(label=f"{i}") for i in range(10)]
fake_inputs = [ServiceInput(label=f"{i}") for i in range(10)]


def can_connect(from_output, to_input, units_registry):
    # O(constant) algorithm
    return from_output == to_input


@pytest.mark.skip(reason="benchmark is only used for development")
@pytest.mark.benchmark(max_time=0.5, min_rounds=1)
@pytest.mark.parametrize(
    "from_port,to_port",
    itertools.product(fake_outputs, fake_inputs),
    ids=lambda p: p.label,
)
def test_can_connect_with_units_with_benchmark(
    benchmark, from_port: ServiceOutput, to_port: ServiceInput, ureg: UnitRegistry
):
    # WARNING: assumes the following convention for the fixture data:
    #   - two ports are compatible if they have the same title
    # WARNING: this probably will change with the demo_units service
    # is modified. At that point, please create a fixture in this test-suite
    # and copy&paste inputs/outputs above
    expected_compatible = from_port.label == to_port.label

    # NOTE: units_registry *might* contain some cache, that is the
    # reason why there is a deviation
    are_compatible = benchmark(
        can_connect,
        from_output=from_port,
        to_input=to_port,
        units_registry=ureg,
    )

    assert are_compatible == expected_compatible
