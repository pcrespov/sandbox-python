from pydantic import BaseSettings, Field
from settingslib.base_settings import BaseCustomSettings

class MyModuleSettings(BaseCustomSettings):
    """
        Settings for Module 1
    """
    MYMODULE_VALUE: int = Field(..., description="Some value for module 1")
