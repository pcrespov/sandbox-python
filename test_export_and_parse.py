from pydantic import BaseModel, Field


class A(BaseModel):
    b: int  # int, non-nullable, required
    e: str | None  # str, nullable, required
    a: str | None = None  # str, nullable, w/ default, not-required
    c: str = Field(None)  # str, non-nullable, not-required


# Used for API schema
class OutputSchema(BaseModel):
    n: int  # int, non-nullable, required
    d: str = "default"  # str, non-nullable, w/ default, not-required
    child: A  # A, non-nullable, required, nested


def test_export_options():
    # data response
    output = {
        "n": 123,
        "child": {"b": 3, "e": None},
        "d": "default",  # sets d to its default!
    }

    # model "fills" output attributes using json-schema defaults
    data = OutputSchema.parse_obj(output).dict()
    assert data == {
        "n": 123,
        "child": {
            "a": None,
            "b": 3,
            "c": None,
            "e": None,
        },
        "d": "default",
    }

    # this is a case in which exclude_unset makes
    data1 = OutputSchema.parse_obj(output).dict(exclude_unset=True)
    assert data1 == {
        "n": 123,
        "child": {
            "b": 3,
            "e": None,
        },
        "d": "default",
    }

    data2 = OutputSchema.parse_obj(output).dict(exclude_unset=False)
    assert data2 == data
    assert data2 == {
        "n": 123,
        "child": {
            "a": None,
            "b": 3,
            "c": None,
            "e": None,
        },
        "d": "default",
    }

    # Since only not-required can be unset, is there a different w.r.t exclude_unset=True ?
    data3 = OutputSchema.parse_obj(output).dict(exclude_defaults=True)
    # aha, so it also exclude values that were set to its defaults!
    # this can be handy when the client uses the jsonschema
    # to determine the defaults
    assert data3 == {
        "n": 123,
        "child": {
            "b": 3,
            "e": None,  # <--- does not add this but WHY? it is NOT a default!
        },
    }
    assert data3 != data1

    # and both?
    data4 = OutputSchema.parse_obj(output).dict(
        exclude_defaults=True, exclude_unset=True
    )
    assert data4 == {
        "n": 123,
        "child": {
            "b": 3,
        },
    }
