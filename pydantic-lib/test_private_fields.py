from textwrap import indent
from typing import Optional
from pydantic import BaseModel, validator, Field, ValidationError,
from pydantic.fields import ModelField


class Node(BaseModel):
    value: int

    value1: Optional[int] = Field(None, exclude=True)
    value2: Optional[int] = Field(None, exclude=True)

    class Config:
        underscore_attrs_are_private = True
        validate_assignment = True

    @validator("value", "value1", "value2")
    @classmethod
    def check_value(cls, v, values, field: ModelField, config, **kwargs):
        print("->", f"{field} -> ", v, values)
        return v


def test_it():

    n = Node(value=1)
    print(Node.schema_json(indent=2))

    try:
        n.value = 2
        n.value1 = "33"
        n.value2 = "fail validation"
    except ValidationError as err:
        print(err)

    n.value1 = 33

    print(n.json(indent=1))


from pydantic import AnyUrl

def test_it():
    url = "http://172.16.8.68:9001/simcore/0ba2d0d6-c538-11ec-867d-02420a00003e/23e3d33b-34c4-4862-abc5-f5eba51ded1d/single_number.txt?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=12345678/20220429/us-east-1/s3/aws4_request&X-Amz-Date=20220429T193544Z&X-Amz-Expires=259200&X-Amz-SignedHeaders=host&X-Amz-Signature=a5df93f4ad79357d081553a5584977d4623552573bd77f3963241ca107abd98a"
    parse_obj_as(AnyUrl, url)
