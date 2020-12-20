from typing import Optional
from pydantic import BaseModel


class User(BaseModel):
    name: str
    surname: Optional[str] = "str-default"
    address: Optional[str] = None
    age: Optional[int]


user = User(name="foo")   