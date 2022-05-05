# pylint: disable=redefined-outer-name
# pylint: disable=unused-argument
# pylint: disable=unused-variable

""" Tests subtle details about pydantic models

This test suite intends to "freeze" some concepts/invariants from pydantic upon which we are going
to build this libraries.

This serves the purpose of both as introduction and as a way to guarantee that future versions of pydantic
would still have these invariants.

"""

from typing import Optional

from pydantic import BaseModel, validator
from pydantic.fields import ModelField, Undefined

# HELPERS --------------------------------------------------------------------------------------


def assert_field_specs(
    model_cls, name, is_required, is_nullable, explicit_default, defaults
):
    field: ModelField = model_cls.__fields__[name]
    print(field, field.field_info)

    assert field.required == is_required
    assert field.allow_none == is_nullable
    assert field.field_info.default == explicit_default

    assert field.default == defaults
    if field.required:
        # in this case, default is not really used
        assert field.default is None


# FIXTURES --------------------------------------------------------------------------------------


class MyModel(BaseModel):
    VALUE: int
    VALUE_DEFAULT: int = 42

    VALUE_NULLABLE_REQUIRED: Optional[int] = ...  # type: ignore
    VALUE_NULLABLE_OPTIONAL: Optional[int]

    VALUE_NULLABLE_DEFAULT_VALUE: Optional[int] = 42
    VALUE_NULLABLE_DEFAULT_NULL: Optional[int] = None

    # Other ways to write down "required" is using ...
    VALUE_ALSO_REQUIRED: int = ...  # type: ignore

    @validator("*", pre=True)
    @classmethod
    def parse_none(cls, v, values, field: ModelField):
        # WARNING: In nullable fields, envs equal to null or none are parsed as None !!
        if field.allow_none:
            if isinstance(v, str) and v.lower() in ("null", "none"):
                return None
        return v


# TESTS --------------------------------------------------------------------------------------


def test_fields_declarations():
    # NOTE:
    #   - optional = not required => defaults to some explicit or implicit value
    #   - nullable = value 'None' is allowed (term borrowed from sql)

    assert_field_specs(
        MyModel,
        "VALUE",
        is_required=True,
        is_nullable=False,
        explicit_default=Undefined,
        defaults=None,
    )

    assert_field_specs(
        MyModel,
        "VALUE_DEFAULT",
        is_required=False,
        is_nullable=False,
        explicit_default=42,
        defaults=42,
    )

    assert_field_specs(
        MyModel,
        "VALUE_NULLABLE_REQUIRED",
        is_required=True,
        is_nullable=True,
        explicit_default=Ellipsis,
        defaults=None,
    )

    assert_field_specs(
        MyModel,
        "VALUE_NULLABLE_OPTIONAL",
        is_required=False,
        is_nullable=True,
        explicit_default=Undefined,  # <- difference wrt VALUE_NULLABLE_DEFAULT_NULL
        defaults=None,
    )

    # VALUE_NULLABLE_OPTIONAL interpretation has always been confusing
    #  to me but effectively it is equivalent to VALUE_NULLABLE_DEFAULT_NULL.
    #  The only difference is that in one case the default is implicit and in the other explicit

    assert_field_specs(
        MyModel,
        "VALUE_NULLABLE_DEFAULT_VALUE",
        is_required=False,
        is_nullable=True,
        explicit_default=42,
        defaults=42,
    )

    assert_field_specs(
        MyModel,
        "VALUE_NULLABLE_DEFAULT_NULL",
        is_required=False,
        is_nullable=True,
        explicit_default=None,  # <- difference wrt VALUE_NULLABLE_OPTIONAL
        defaults=None,
    )

    assert_field_specs(
        MyModel,
        "VALUE_ALSO_REQUIRED",
        is_required=True,
        is_nullable=False,
        explicit_default=Ellipsis,
        defaults=None,
    )
