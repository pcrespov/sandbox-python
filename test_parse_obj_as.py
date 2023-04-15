from typing import Optional, TypedDict

from pydantic import BaseModel, Extra, parse_obj_as


class EmptyModel(BaseModel):
    ...

    class Config:
        extra = Extra.forbid


class EmptyDict(TypedDict):
    ...


result = parse_obj_as(EmptyDict, {})
print(result)


result = parse_obj_as(EmptyDict, {"foo": 3})
print(result)


result = parse_obj_as(EmptyModel, {})
print(result)


result = parse_obj_as(EmptyModel, {"foo": 3})
print(result)


result = parse_obj_as(Optional[EmptyDict], {})
print(result)
