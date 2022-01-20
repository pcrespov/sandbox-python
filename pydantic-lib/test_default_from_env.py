import json
import os
import types
from email.policy import default
from typing import Optional

import pytest
from pydantic import BaseConfig, BaseSettings, ValidationError
from pydantic.error_wrappers import ErrorWrapper
from pydantic.fields import Field, ModelField, Undefined


def default_capture_from_env(env):
    def _capture():
        return os.environ[env]

    return _capture


class AutoDefaultFromEnvError(ValidationError):
    ...


def create_settings_from_env(model_cls, field):
    # Keeps a reference of field but MUST nothing should be modified there
    # cannot pass only field.type_ because @prepare_field still not resolved!

    def _capture():
        field_settings_cls = field.type_
        try:
            return field_settings_cls()

        except ValidationError as err:
            if field.allow_none:
                return None

            raise AutoDefaultFromEnvError(
                errors=[
                    ErrorWrapper(e.exc, (field.name,) + e.loc_tuple())
                    for e in err.raw_errors
                ],
                model=model_cls,
            ) from err

    return _capture


@pytest.fixture
def model_class_factory():
    def _create_model():
        class BaseCustomSettings(BaseSettings):
            class Config(BaseConfig):
                @classmethod
                def prepare_field(cls, field: ModelField) -> None:
                    super().prepare_field(field)

                    field_type = field.type_[0]  # FIXME: probably not resolved
                    auto_default_from_env = field.field_info.extra.get(
                        "auto_default_from_env", False
                    )

                    if issubclass(field_type, BaseCustomSettings):

                        if auto_default_from_env:

                            assert field.field_info.default is Undefined
                            assert field.field_info.default_factory is None

                            # change to
                            field.default_factory = create_settings_from_env(cls, field)

                            # Undefined required -> required=true
                            # Undefined default and no factor -> default=None
                            field.required = False

                    elif issubclass(BaseSettings, field._type):
                        raise ValueError(
                            f"{cls}.{field.name} of type {field_type} must inherit from BaseCustomSettings"
                        )

                    elif auto_default_from_env:
                        raise ValueError(
                            "auto_default_from_env=True can only be used in BaseCustomSettings subclasses"
                            f"but field {cls}.{field.name} is {field_type} "
                        )

        class S(BaseCustomSettings):
            S_VALUE: int

        class M(BaseCustomSettings):
            # VALUE: int = Field(default_factory=default_capture_from_env("M_DEFAULT"))
            ## SUB_SETTINGS: P = Field(default_factory=capture_settings_from_env(P))

            VALUE: S
            VALUE_DEFAULT: S = S(S_VALUE=42)
            VALUE_CONFUSING: S = None

            VALUE_NULLABLE_REQUIRED: Optional[S] = ...  # type: ignore
            VALUE_NULLABLE_OPTIONAL: Optional[S]

            VALUE_NULLABLE_DEFAULT_VALUE: Optional[S] = S(S_VALUE=42)
            VALUE_NULLABLE_DEFAULT_NULL: Optional[
                S
            ] = None  # defaults disabled but only explicit enabled

            VALUE_NULLABLE_DEFAULT_ENV: Optional[S] = Field(
                auto_default_from_env=True
            )  # defaults enabled but if not exists, it disables
            VALUE_DEFAULT_ENV: S = Field(
                auto_default_from_env=True
            )  # cannot be disabled

        return M

    return _create_model


def test_1(monkeypatch, model_class_factory):

    S42 = json.dumps({"S_VALUE": 42})
    
    M = model_class_factory()

    with monkeypatch.context() as patch:

        patch.setenv("S_VALUE", "1")
        patch.setenv("VALUE", S42)

        obj = M()
        print(obj.json(indent=2))
        print("-" * 20)
