import pytest
from pydantic import BaseModel, Field, ValidationError


class MyModel(BaseModel):
    x: int = Field(...)  # non-nullable required
    y: int | None = Field(...)  # nullable and required
    z: int | None = Field(None)  # nullable and optional
    w: int = Field(None)  # non-nullable and optional


def test_it():
    # set only required
    m = MyModel(x=1, y=None)

    assert m.dict() == {"x": 1, "y": None, "z": None, "w": None}
    assert m.dict(exclude_defaults=True) == {"x": 1, "y": None}
    assert m.dict(exclude_unset=True) == {"x": 1, "y": None}
    assert m.dict(exclude_none=True) == {
        "x": 1
    }  # NOTE that w is set intenally to NOne even if it is not nullable!

    # set also z!
    n = MyModel(x=1, y=None, z=None)
    assert n.dict() == {"x": 1, "y": None, "z": None, "w": None}
    assert n.dict(exclude_defaults=True) == {"x": 1, "y": None}
    assert n.dict(exclude_unset=True) == {"x": 1, "y": None, "z": None}  # <----
    assert n.dict(exclude_none=True) == {"x": 1}

    MyModel(x=1, y=None, z=None, w=None)  # allowed to set w!!

    with pytest.raises(ValidationError) as err_info:
        MyModel(x=None, y=None, z=None, w=None)  # NOT allo

    validation_error = err_info.value
    assert validation_error.errors()[0]["type"] == "type_error.none.not_allowed"

    #
    # pydantic.error_wrappers.ValidationError: 1 validation error for MyModel
    #    x
    # none is not an allowed value (type=type_error.none.not_allowed)
