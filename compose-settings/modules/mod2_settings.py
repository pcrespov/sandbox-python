from pydantic import BaseSettings
from . import _base

class MyModule2Settings(BaseSettings):
    """ Settings for module 2 """

    some_other_value: int

    class Config(_base.CommonConfig):
        pass