from pydantic import BaseModel


class BaseItem(BaseModel):
    id: str
    name: str


class Company(BaseItem):
    attr1: str
    attr2: str



