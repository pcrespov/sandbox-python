import os
from typing import Optional

from pydantic import BaseSettings, validator
from pydantic.fields import ModelField, Undefined


def assert_field_specs(
    settings_cls, name, is_required, is_nullable, explicit_default, defaults
):
    field: ModelField = settings_cls.__fields__[name]
    print(field, field.field_info)
    assert field.required == is_required
    assert field.allow_none == is_nullable
    assert field.field_info.default == explicit_default

    assert field.default == defaults
    if field.required:
        assert field.default is None


class Settings(BaseSettings):
    VALUE: int
    VALUE_DEFAULT: int = 42

    VALUE_NULLABLE_REQUIRED: Optional[int] = ...
    VALUE_NULLABLE_OPTIONAL: Optional[int]

    VALUE_NULLABLE_DEFAULT_VALUE: Optional[int] = 42
    VALUE_NULLABLE_DEFAULT_NULL: Optional[int] = None

    # Other ways to write down "required" is using ...
    VALUE_ALSO_REQUIRED: int = ...

    # VALUE_NULLABLE_OPTIONAL interpretation has always been confusing to me but effectively
    #  it is equivalent to VALUE_NULLABLE_DEFAULT_NULL. The only difference
    #  is that in one case the default is implicit and in the other explicit


    @validator("*", pre=True)
    def parse_none(cls, v, values, field: ModelField):
        """ For nullable fields, env vars set to null or none are parsed as None"""
        if field.allow_none:
            if isinstance(v, str) and  v.lower() in ("null", "none"):
                return None
        return v



def test_fields_declarations():
    # optional = not required => defaults to some explicit or implicit value
    # nullable = value 'None' is allowed

    assert_field_specs(
        Settings,
        "VALUE",
        is_required=True,
        is_nullable=False,
        explicit_default=Undefined,
        defaults=None,
    )
    assert_field_specs(
        Settings,
        "VALUE_DEFAULT",
        is_required=False,
        is_nullable=False,
        explicit_default=42,
        defaults=42,
    )

    assert_field_specs(
        Settings,
        "VALUE_NULLABLE_REQUIRED",
        is_required=True,
        is_nullable=True,
        explicit_default=Ellipsis,
        defaults=None,
    )
    assert_field_specs(
        Settings,
        "VALUE_NULLABLE_OPTIONAL",
        is_required=False,
        is_nullable=True,
        explicit_default=Undefined,
        defaults=None,
    )

    assert_field_specs(
        Settings,
        "VALUE_NULLABLE_DEFAULT_VALUE",
        is_required=False,
        is_nullable=True,
        explicit_default=42,
        defaults=42,
    )
    assert_field_specs(
        Settings,
        "VALUE_NULLABLE_DEFAULT_NULL",
        is_required=False,
        is_nullable=True,
        explicit_default=None,
        defaults=None,
    )

    assert_field_specs(
        Settings,
        "VALUE_ALSO_REQUIRED",
        is_required=True,
        is_nullable=False,
        explicit_default=Ellipsis,
        defaults=None,
    )


def test_1(monkeypatch):

    # from init
    settings1 = Settings(VALUE=1, VALUE_ALSO_REQUIRED=10, VALUE_NULLABLE_REQUIRED=None)


    # sets ONLY required ones
    monkeypatch.setenv("VALUE", "1")
    monkeypatch.setenv("VALUE_ALSO_REQUIRED", "10")
    monkeypatch.setenv("VALUE_NULLABLE_REQUIRED", "null") # WARNING: this would not work w/o ``parse_none`` validator!

    settings2 = Settings()
    print(settings2.json(exclude_unset=True, indent=2))


    assert settings1 == settings2


