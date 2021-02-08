from pydantic import BaseSettings, Field
from pydantic.error_wrappers import ValidationError
import os


class MySettings(BaseSettings):
    foo: bool = Field(..., env=["FOOLISH", "FOOOO"])


os.environ["FOOLISH"] = "YES"
os.environ["FOOOO"] = "0"

print(MySettings().json(indent=2))


os.environ.pop("FOOLISH")
print(MySettings().json(indent=2))


os.environ.pop("FOOOO")
try:
    assert not MySettings().json(indent=2)
except ValidationError as err:
    print("I expected", err)
