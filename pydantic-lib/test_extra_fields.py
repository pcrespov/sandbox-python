from typing import Any

from pydantic import BaseModel, Field


#
# Can use the extra field to mark
#
class A(BaseModel):
    x: int = Field(..., x_mark_public=True)
    y: int
    z: int = Field(..., x_mark_public=False)


class B(BaseModel):
    a: A
    b: int = Field(..., x_mark_public=True)
    c: A = Field(..., x_mark_public=True)  # ??
    d: list[A]


def get_marked_fields(model_cls: type[BaseModel], mark: str) -> dict[str, Any]:
    assert mark.startswith("x_mark_")  # nosec
    fname_to_mval = {}
    for f in model_cls.__fields__.values():
        if mark in f.field_info.extra:
            fname_to_mval[f.name] = f.field_info.extra[mark]
    return fname_to_mval


def test_it():
    # what use we give to the value?
    # how do we interpret the filter hierarchically?
    # what if a model is in container (i.e. list, dict etc)?

    assert get_marked_fields(A, "x_mark_public") == {"x": True, "z": False}

    #
    assert get_marked_fields(B, "x_mark_public") == {
        "b": True,
        "c": {"x": True, "z": False},
    }

    # so later they can be used in include/exclude
    ## https://pydantic-docs.helpmanual.io/usage/exporting_models/#model-and-field-level-include-and-exclude

    THIS IS UNFINISEHD!
