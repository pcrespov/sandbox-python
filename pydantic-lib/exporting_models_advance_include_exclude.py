#
# SEE https://pydantic-docs.helpmanual.io/usage/exporting_models/#advanced-include-and-exclude
#
from pydantic import BaseModel
from typing import Dict
from uuid import uuid4


class BarModel(BaseModel):
    whatever: int
    other: str = ""


class FooBarModel(BaseModel):
    banana: float
    foo: str
    bar: BarModel
    bars: Dict[str, BarModel]


m = FooBarModel(
    banana=3.14,
    foo="hello",
    bar={"whatever": 123},
    bars={
        str(uuid4()): {"whatever": 1, "other": "one"},
        str(uuid4()): {"whatever": 2, "other": "two"},
    },
)

# something like {"bars": { "*" : {"other"} }}
print(m.json(include={"bars": { key: {"other"} for key in m.bars } }))

print(m)
