import os
from contextlib import suppress
from typing import FrozenSet

from modules.mod1_settings import MyModuleSettings
from modules.mod2_settings import AnotherModuleSettings
from settingslib.base_settings import BaseCustomSettings
from settingslib.postgres import PostgresSettings

from pydantic import class_validators
from pydantic.error_wrappers import ValidationError
from pydantic.fields import FieldInfo, Field


class Settings(BaseCustomSettings):
    APP_HOST: str
    APP_PORT: int = 3

    APP_POSTGRES: PostgresSettings
    APP_MODULE_1: MyModuleSettings = Field(None, description="Some Module Example")
    APP_MODULE_2: AnotherModuleSettings

    @classmethod
    def create_from_env(cls) -> "Settings":
        # Builds defaults at this point
        for name, default_cls in [
            ("APP_POSTGRES", PostgresSettings),
            ("APP_MODULE_1", MyModuleSettings),
            ("APP_MODULE_2", AnotherModuleSettings),
        ]:
            with suppress(ValidationError):
                default = default_cls()
                field_obj = cls.__fields__[name]
                field_obj.default = default
                field_obj.required = False

        return cls()
