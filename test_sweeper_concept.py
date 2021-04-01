import pytest
from itertools import product

@pytest.fixture(params=product(range(3), range(3)))
def ds1(request):
    print("\nds1 -> x,y=", request.param)
    return request.param

@pytest.fixture( params=range(4))
def ds2(request):
    print("ds2 -> z=", request.param)
    return request.param

@pytest.fixture(params=[1,5,7])
def ds3(request):
    print("ds3 -> w=", request.param)
    return request.param

@pytest.fixture
def de1(ds1, ds2):
    x,_ = ds1
    z = ds2
    res = x*z
    print("de1(x,z)=", "%3.2f"%res)
    return res

@pytest.fixture
def de2(ds1, ds3, de1):
    _,y = ds1
    w = ds3
    res = y/w+de1
    print("de2(y,w,de1)=", "%3.2f"%res)
    return res


def test_dc(de1, de2):
    print("Storing result", "%3.2f"%de1)
    print("Storing result", "%3.2f"%de2)

