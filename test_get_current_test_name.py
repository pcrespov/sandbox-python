import pytest
import inspect


# Request fixture
# https://docs.pytest.org/en/latest/reference/reference.html?highlight=request#request
#
#


def test_name1(request):

    testname = request.node.name

    assert testname == inspect.currentframe().f_code.co_name
