from typing import Any, Dict, Mapping, TypedDict
from collections import abc
from pydantic import BaseModel


class MyDict(TypedDict):
    a: int
    b: int


class A(BaseModel):
    x: dict[str, Any]
    y: Dict[str, Any]
    z: Mapping[str, Any]


def test_types():

    # this is a way to define a dict as a structured dataset
    c = MyDict(a=1, b=2)
    assert isinstance(c, dict)
    assert isinstance(c, abc.Mapping)
    assert isinstance(c, abc)

    # notice that these are NOT the same
    assert abc.Mapping is not Mapping
    assert dict is not Dict

    assert A.schema() == {
        "title": "A",
        "type": "object",
        "properties": {
            "x": {"title": "X", "type": "object"},
            "y": {"title": "Y", "type": "object"},
            "z": {"title": "Z", "type": "object"},
        },
        "required": ["x", "y", "z"],
    }

    # and  we can combine as we wish
    a = A(x=c, y={"x": 1, "y": 2}, z=c)
    print(a.json(indent=2))

    # Q: So, what difference it makes to define dict, Dict, Mapping.
    #   Dict is included in Mapping, so it makes it more general. OK, but
    #   what about dict vs Dict?? What is the difference
