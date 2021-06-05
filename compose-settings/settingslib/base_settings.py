from pydantic import Extra, BaseSettings

# https://pydantic-docs.helpmanual.io/usage/model_config/


class BaseCustomSettings(BaseSettings):
    class Config:
        env_file = '.env'
        case_sensitive = False
        extra = Extra.forbid
        allow_mutation = False
        frozen = True
        validate_all = True

