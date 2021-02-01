# https://pydantic-docs.helpmanual.io/usage/models/#custom-root-types

from typing import List

from pydantic import BaseModel, Field


class Pet(BaseModel):
    animal: str

class Pets(BaseModel):
    __root__: List[Pet] = []


print(Pets(__root__=[Pet(animal=t) for t in ["dog", "cat"]]))
print(Pets(__root__=None))






class ResourceHit(BaseModel):
    rrid: str = Field(..., alias="rid")
    # original_id: str
    name: str


class ListOfResourceHits(BaseModel):
    __root__: List[ResourceHit]


data = [{"name": "cryoSPARC", "original_id": "SCR_016501", "rid": "SCR_016501"}]


for hits in [ListOfResourceHits(__root__=data), ListOfResourceHits.parse_obj(data)]:
    print(hits.dict())
    print(hits.json(indent=2))
    print(hits.dict()['__root__'])
