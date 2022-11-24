import itertools
from dataclasses import dataclass
from typing import NamedTuple, TypedDict

import pytest
from faker import Faker
from pydantic import BaseModel
from pydantic.dataclasses import dataclass as pydantic_dataclass


class TagTypeDict(TypedDict, total=True):
    id: int
    name: str
    description: str
    color: str
    # access rights
    read: bool
    write: bool
    delete: bool


class TagNameTuple(NamedTuple):
    id: int
    name: str
    description: str
    color: str
    # access rights
    read: bool
    write: bool
    delete: bool


@dataclass  # (slots=True)
class TagDataClass:
    id: int
    name: str
    description: str
    color: str
    # access rights
    read: bool
    write: bool
    delete: bool


class TagPydanticModel(BaseModel):
    id: int
    name: str
    description: str
    color: str
    # access rights
    read: bool
    write: bool
    delete: bool


@pydantic_dataclass
class TagPydanticDataclass:
    id: int
    name: str
    description: str
    color: str
    # access rights
    read: bool
    write: bool
    delete: bool


@pytest.fixture
def data(faker: Faker):
    return {
        "id": faker.pyint(),
        "name": faker.pystr(),
        "description": faker.pystr() * 30,
        "color": faker.pystr(),
        "read": faker.pybool(),
        "write": faker.pybool(),
        "delete": faker.pybool(),
    }


@pytest.mark.parametrize(
    "cls,n",
    itertools.product(
        (
            TagPydanticDataclass,
            TagPydanticModel,
            TagTypeDict,
            TagDataClass,
            TagNameTuple,
        ),
        (1000, 10000, 100000),
    ),
)
def test_speed(benchmark, cls, n, data):
    build = lambda: [cls(**data) for _ in range(n)]
    d = benchmark(build)
