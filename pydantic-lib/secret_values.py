import os
from pydantic import BaseModel, SecretBytes, SecretStr, BaseSettings


class Settings(BaseSettings):
    SECRET_KEY: SecretStr
    SECRET_KEY2: SecretBytes


os.environ["SECRET_KEY"] = "REPLACE ME with a key of at least length 32."
os.environ["SECRET_KEY2"] = "REPLACE ME with a key of at least length 32."

settings = Settings()

print(settings.SECRET_KEY.get_secret_value())
print(settings.SECRET_KEY2.get_secret_value())

assert (
    settings.SECRET_KEY.get_secret_value().encode("utf-8")
    == settings.SECRET_KEY2.get_secret_value()
)
