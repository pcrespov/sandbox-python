import random


from typing import Type
from pydantic import BaseModel


def create_fake_data_from_schema(
    model_cls: Type[BaseModel], *, include_defaults: bool = False
):

    data = {}
    for field in model_cls.__fields__.values():
        if field.required:
            # use examples
            data[field.name] = random.choice(field.field_info.extra.get("examples"))

            # use type in combination with faker (hypothesis? i guess as well)
            # check on field.type_

            # defaults?
            field.default

            # check on Config.schema_extra["example"]
            # check on Config.schema_extra["examples"]


import pytest


class A(BaseModel):
    x: int


@pytest.mark.parametrize("model_cls", [A])
def test_faker(model_cls: Type[BaseModel]):

    data = create_fake_data_from_schema(model_cls)
    model = model_cls.parse_obj(data)
