import pytest
import sys


@pytest.fixture(scope="session")
def multiport_simulation():
    # Notice that this is called ONLY once because of the scope!
    print("Producing input files from multiport simulation")
    return "MultiFoo"


@pytest.fixture(params=list(range(5)))
def port(request):
    # same trick as with z_sample
    return request.param


@pytest.fixture
def simulation_result(port, multiport_simulation):
    print(f"Running simulation {port} from {multiport_simulation}")
    return f"result from port {port} in {multiport_simulation}"


@pytest.fixture
def trp(port, simulation_result) -> float:
    # See here how the port gets in sync with simulaton_result
    # because of the dependencies
    #
    print(f"Computing trp for {port} from {simulation_result}")
    return 3 * port  # fake computed TRP


@pytest.fixture(params=[1.0, 2.0, 4.8, 5.3])
def z_sample(request):
    # this fixture makes parametrized fixtures more readable
    # since they need this special "request" fixture
    # https://docs.pytest.org/en/stable/fixture.html#parametrizing-fixtures
    z = request.param
    return z


@pytest.fixture
def surface(z_sample, simulation_result):
    s = f"z={z_sample} from {simulation_result}"
    print("extracting surface at", s)
    return s


def test_compute_spd(surface, trp):
    # this computation trigger the full dependencies chain
    print("computing SPD on", surface, "normalized to", trp, "watts")


if __name__ == "__main__":
    sys.exit(pytest.main(["-vv", "-s", __file__]))
