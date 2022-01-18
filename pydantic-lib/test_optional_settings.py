
import os
from typing import Optional

from pydantic import BaseSettings
from pydantic.fields import ModelField, Undefined


def assert_field_specs(settings_cls, name, is_required, is_nullable, explicit_default, default):
    field: ModelField = settings_cls.__fields__[name]
    print(field, field.field_info)
    assert field.required == is_required
    assert field.allow_none == is_nullable
    assert field.field_info.default == explicit_default
    assert field.default == default



    

class Settings(BaseSettings):
    VALUE: int
    VALUE_DEFAULT: int = 42 
    
    VALUE_NULLABLE_REQUIRED: Optional[int] = ...
    VALUE_NULLABLE_OPTIONAL: Optional[int]

    VALUE_NULLABLE_DEFAULT_VALUE: Optional[int] = 42
    VALUE_NULLABLE_DEFAULT_NULL: Optional[int] = None


    # Other ways to write down "required" is using ...
    VALUE_ALSO_REQUIRED: int = ...



def test_declaration():
    # optional = not required => defaults to some explicit or implicit value
    # nullable = value 'None' is allowed

    assert_field_specs(Settings, "VALUE", is_required=True, is_nullable=False, explicit_default=Undefined, default=None)
    assert_field_specs(Settings, "VALUE_DEFAULT", is_required=False, is_nullable=False, explicit_default=42, default=42)

    assert_field_specs(Settings, "VALUE_NULLABLE_REQUIRED", is_required=True, is_nullable=True, explicit_default=Ellipsis, default=None)
    assert_field_specs(Settings, "VALUE_NULLABLE_OPTIONAL", is_required=False, is_nullable=True, explicit_default=Undefined, default=None)

    assert_field_specs(Settings, "VALUE_NULLABLE_DEFAULT_VALUE", is_required=False, is_nullable=True, explicit_default=42, default=42)
    assert_field_specs(Settings, "VALUE_NULLABLE_DEFAULT_NULL", is_required=False, is_nullable=True, explicit_default=None, default=None)

    assert_field_specs(Settings, "VALUE_ALSO_REQUIRED", is_required=True, is_nullable=False, explicit_default=Ellipsis, default=None)


def test_parse_from_env(monkeypatch):

    monkeypatch.setenv("VALUE", "1")
    monkeypatch.setenv("VALUE_ALSO_REQUIRED", "10")

    monkeypatch.setenv("VALUE_NULLABLE", "null")
    monkeypatch.setenv("VALUE_NULLABLE_ALSO_REQUIRED", "null")




    data = { key:os.environ[key] for key in ("VALUE", "VALUE_ALSO_REQUIRED", "VALUE_NULLABLE", "VALUE_NULLABLE_ALSO_REQUIRED")}
    settings1 = Settings.parse_obj(data)

    print(settings1.json(exclude_unset=True, indent=2))


    settings = Settings()
    print(settings.json(exclude_unset=True, indent=2))


def test_construct(monkeypatch):
    settings1 = Settings(VALUE=1, VALUE_ALSO_REQUIRED=10, VALUE_NULLABLE=None, VALUE_NULLABLE_ALSO_REQUIRED=None)
    print(settings1.json(exclude_unset=True, indent=2))


