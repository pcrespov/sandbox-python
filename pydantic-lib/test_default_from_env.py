import json
import os
import types
from contextlib import contextmanager
from email.policy import default
from functools import cached_property
from pathlib import Path
from typing import Optional, get_args

import pytest
from pydantic import BaseConfig, BaseSettings, Extra, ValidationError, validator
from pydantic.error_wrappers import ErrorWrapper
from pydantic.fields import Field, ModelField, Undefined
from pydantic.types import SecretStr

# HELPERS --------------------------------------------------------------------


def get_attrs_tree(obj):
    # long version of json.dumps({ k:str(getattr(field,k)) for k in ModelField.__slots__ } )
    tree = {}
    for name in obj.__class__.__slots__:
        value = getattr(obj, name)
        if hasattr(value.__class__, "__slots__"):
            tree[name] = get_attrs_tree(value)
        else:
            tree[name] = f"{value}"

    return tree


def print_defaults(model_cls):
    for field in model_cls.__fields__.values():
        print(field.name, ":", end="")
        try:
            default = field.get_default()
            print(default, type(default))
        except ValidationError as err:
            print(err)

def dumps_model_class(model_cls):
    d = {field.name: get_attrs_tree(field) for field in model_cls.__fields__.values()}
    return json.dumps(d, indent=2)

# IMPLEMENTATION ---------------------------------------------------------------


class AutoDefaultFromEnvError(ValidationError):
    ...


def create_settings_from_env(field):
    # Keeps a reference of field but MUST nothing should be modified there
    # cannot pass only field.type_ because @prepare_field still not resolved!

    def _capture():
        settings_cls = field.outer_type_ # FIXME: this is wrong
        sub_settings_cls = field.type_
        try:
            return sub_settings_cls()

        except ValidationError as err:
            if field.allow_none:
                return None

            raise AutoDefaultFromEnvError(
                errors=[
                    ErrorWrapper(e.exc, (field.name,) + e.loc_tuple())
                    for e in err.raw_errors
                ],
                model=settings_cls,
            ) from err

    return _capture


class BaseCustomSettings(BaseSettings):

    @validator("*", pre=True)
    @classmethod
    def parse_none(cls, v, field: ModelField):
        # WARNING: In nullable fields, envs equal to null or none are parsed as None !!
        if field.allow_none:
            if isinstance(v, str) and v.lower() in ("null", "none"):
                return None
        return v

    class Config(BaseConfig):
        case_sensitive = False
        extra = Extra.forbid
        allow_mutation = False
        frozen = True
        validate_all = True
        json_encoders = {SecretStr: lambda v: v.get_secret_value()}
        keep_untouched = (cached_property,)

        @classmethod
        def prepare_field(cls, field: ModelField) -> None:
            super().prepare_field(field)

            # print("field:", json.dumps(get_attrs_tree(field), indent=2))

            auto_default_from_env = field.field_info.extra.get(
                "auto_default_from_env", False
            )

            field_type = field.type_
            if args := get_args(field_type):
                # TODO: skip all the way if none of these types
                field_type = next(a for a in args if issubclass(a, BaseSettings))

            if issubclass(field_type, BaseCustomSettings):

                if auto_default_from_env:

                    assert field.field_info.default is Undefined
                    assert field.field_info.default_factory is None

                    field.default_factory = create_settings_from_env(field)

                    # Undefined required -> required=true
                    # Undefined default and no factor -> default=None
                    field.required = False

            elif issubclass(field_type, BaseSettings):
                raise ValueError(
                    f"{cls}.{field.name} of type {field_type} must inherit from BaseCustomSettings"
                )

            elif auto_default_from_env:
                raise ValueError(
                    "auto_default_from_env=True can only be used in BaseCustomSettings subclasses"
                    f"but field {cls}.{field.name} is {field_type} "
                )


# FIXTURES ---------------------------------------------------------------


@pytest.fixture
def model_class_factory():
    def _create_model():
        class S(BaseCustomSettings):
            S_VALUE: int

        class M1(BaseCustomSettings):
            VALUE: S
            VALUE_DEFAULT: S = S(S_VALUE=42)
            VALUE_CONFUSING: S = None

            VALUE_NULLABLE_REQUIRED: Optional[S] = ...  # type: ignore
            VALUE_NULLABLE_OPTIONAL: Optional[S]

            VALUE_NULLABLE_DEFAULT_VALUE: Optional[S] = S(S_VALUE=42)
            VALUE_NULLABLE_DEFAULT_NULL: Optional[S] = None

            VALUE_NULLABLE_DEFAULT_ENV: Optional[S] = Field(auto_default_from_env=True)
            VALUE_DEFAULT_ENV: S = Field(auto_default_from_env=True)

        class M2(BaseCustomSettings):

            # defaults disabled but only explicit enabled
            VALUE_NULLABLE_DEFAULT_NULL: Optional[S] = None

            # defaults enabled but if not exists, it disables
            VALUE_NULLABLE_DEFAULT_ENV: Optional[S] = Field(auto_default_from_env=True)

            # cannot be disabled
            VALUE_DEFAULT_ENV: S = Field(auto_default_from_env=True)

        return M1, M2

    return _create_model


# TEST ---------------------------------------------------------------
S2 = json.dumps({"S_VALUE": 2})
S3 = json.dumps({"S_VALUE": 3})

def test_1(monkeypatch, model_class_factory):

    M, _ = model_class_factory()
    Path("M.json").write_text(dumps_model_class(M))

    assert M.__fields__["VALUE_NULLABLE_DEFAULT_ENV"].default_factory
    assert M.__fields__["VALUE_DEFAULT_ENV"].default_factory

    assert M.__fields__["VALUE_NULLABLE_DEFAULT_ENV"].get_default() == None
    
    with pytest.raises(AutoDefaultFromEnvError):
        M.__fields__["VALUE_DEFAULT_ENV"].get_default()

    with monkeypatch.context() as patch:

        patch.setenv("S_VALUE", "1")
        patch.setenv("VALUE", S2)
        patch.setenv("VALUE_NULLABLE_REQUIRED", S3)

        print_defaults(M)

        obj = M()

        print(obj.json(indent=2))
        print("-" * 20)
