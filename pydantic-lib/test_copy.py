from xml.dom.minidom import Attr

import pytest
from pydantic import BaseModel


# SEE https://pydantic-docs.helpmanual.io/usage/exporting_models/#modelcopy


class BarModel(BaseModel):
    whatever: int


class FooBarModel(BaseModel):
    banana: float
    foo: str
    bar: BarModel


def test_copy_include():
    m = FooBarModel(banana=3.14, foo="hello", bar={"whatever": 123})

    # notice that this creates a type FooBarModel w/o banana ... then what is the value associated to banana?
    mcopy = m.copy(include={"foo", "bar"})
    assert isinstance(mcopy, FooBarModel)
    assert "banana" in mcopy.__fields__

    # BUT ...
    with pytest.raises(AttributeError) as exc_info:
        mcopy.banana

    assert exc_info.type == AttributeError
    # AttributeError: 'FooBarModel' object has no attribute 'banana'


def test_copy_deep():
    m = FooBarModel(banana=3.14, foo="hello", bar={"whatever": 123})

    assert m.copy().bar == m.bar
    assert m.copy().bar is m.bar

    assert m.copy(deep=True).bar == m.bar
    assert m.copy(deep=True).bar is not m.bar

    # BUT CAREFUL, include/exclude behaves as with a deep copy
    assert m.copy(include={"bar"}).bar == m.bar
    assert m.copy(include={"bar"}).bar is not m.bar

    assert m.copy(include={"bar"}, deep=True).bar == m.bar
    assert m.copy(include={"bar"}, deep=True).bar is not m.bar

    assert m.copy(include={"bar"}, deep=True).json() == m.json(include={"bar"})


def test_copy_exclude():
    m = FooBarModel(banana=3.14, foo="hello", bar={"whatever": 123})

    mcopy = m.copy(exclude={"foo", "bar"})

    assert isinstance(mcopy, FooBarModel)
    assert mcopy == {"banana": 3.14}


def test_copy_updated():
    m = FooBarModel(banana=3.14, foo="hello", bar={"whatever": 123})

    mcopy = m.copy(update={"foo": 55}, deep=True)

    assert isinstance(mcopy, FooBarModel)



# truncating from Extentended to Base -------------------------------------------------


class User(BaseModel):
    id: int
    age: int
    name: str = "John Doe"


class UserExt(User):
    address: str


def test_truncate():

    extuser = UserExt(id=123, age=32, address="newyork Avenue")

    truncated_user1 = extuser.copy(exclude={"address"})
    print(truncated_user1)

    truncated_user2 = User(extra_to_be_truncated=22, **extuser.dict())
    print(truncated_user2)

    assert truncated_user2 == truncated_user1
