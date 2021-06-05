from pydantic import (
    SecretStr,
    conint,
    PostgresDsn,
    Field,
    validator,
    BaseSettings,
)
from typing import Optional
from .base_settings import BaseCustomSettings

PortInt = conint(gt=0, lt=65535)


class PostgresSettings(BaseCustomSettings):
    # entrypoint
    POSTGRES_HOST: str
    POSTGRES_PORT: PortInt = 5432

    # auth
    POSTGRES_USER: str
    POSTGRES_PASSWORD: SecretStr

    # database
    POSTGRES_DB: str = Field(..., description="Database name")

    # pool connection limits
    POSTGRES_MINSIZE: conint(ge=1) = Field(
        1, description="Maximum number of connections in the pool"
    )
    POSTGRES_MAXSIZE: conint(ge=1) = Field(
        50, description="Minimum number of connections in the pool"
    )

    @validator("POSTGRES_MAXSIZE")
    @classmethod
    def _check_size(cls, v, values):
        if not (values["POSTGRES_MINSIZE"] <= v):
            raise ValueError(
                f"assert POSTGRES_MINSIZE={values['POSTGRES_MINSIZE']} <= POSTGRES_MAXSIZE={v}"
            )
        return v


    # HELPERS ---

    def dsn(self):
        return PostgresDsn.build(
            scheme="postgresql",
            user=self.POSTGRES_USER,
            password=self.POSTGRES_PASSWORD.get_secret_value(),
            host=self.POSTGRES_HOST,
            port=f"{self.POSTGRES_PORT}",
            path=f"/{self.POSTGRES_DB}",
        )
