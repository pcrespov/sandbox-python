from pydantic import BaseSettings, Field
from . import _base


class MyModuleSettings(BaseSettings):
    """
        Settings for Module 1
    """
    value: int

    class Config(_base.CommonConfig):
        env_prefix = "MYMODULE_"