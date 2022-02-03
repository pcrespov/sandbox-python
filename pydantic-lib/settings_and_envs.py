from pydantic import BaseSettings, Field
from pydantic.error_wrappers import ValidationError
import os


class MySettings(BaseSettings):
    FOO: bool = Field(..., env=["FOOLISH", "FOOOO"])


os.environ["FOOLISH"] = "YES"
os.environ["FOOOO"] = "0"
os.environ["FOO"] = "0"


obj = MySettings()
print(obj.json(indent=2))
assert obj.dict() == {"FOO": True}


os.environ.pop("FOOLISH")
obj = MySettings()
print(obj.json(indent=2))
assert obj.dict() == {"FOO": False}

os.environ.pop("FOOOO")
try:
    # FOO envvar does not matter
    obj = MySettings()
except ValidationError as err:
    print("I expected", err)
