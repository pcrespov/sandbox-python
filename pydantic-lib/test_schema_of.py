import typing
from cProfile import label
from typing import List

from pydantic import (
    AnyUrl,
    BaseModel,
    EmailStr,
    Field,
    PaymentCardNumber,
    PositiveFloat,
    PositiveInt,
    schema_json_of,
)

# "inputs": {
#     "in_1": {
#         "label": "paramrefs",
#         "description": "reference parameters",
#         "type": List[
#             float
#         ],  # TODO: check how pydantic maps with python with jsonschema
#     },
#     "in_2": {
#         "label": "paramdiff",
#         "description": "diff parameters",
#         "type": List[float],
#     },
#     "in_3": {
#         "label": "diff_or_fact",
#         "description": "Applies difference (true) or factor (false)",
#         "type": bool,
#     },

#     "out_1": {
#         "label": "i",
#         "description": "dimension index that was modified",
#         "type": int,
#     },
#     "out_2": {
#         "label": "paramtestplus",
#         "description": "increased parameter",
#         "type": List[float],
#     },
#     "out_3": {
#         "label": "paramtestminus",
#         "description": "decreased parameter",
#         "type": List[float],
#     },
# },


#
#
# SEE https://swagger.io/docs/specification/media-types/
# SEE https://json-schema.org/draft-04/json-schema-hypermedia.html
# SEE https://apisyouwonthate.com/blog/getting-started-with-json-hyper-schema#link-description-object-ldo
#
#

# This is actually abusing to generate
class InputsSchema(BaseModel):
    in_1: List[float] = Field(
        description="reference parameters", label="paramrefs", xunit="Hz"
    )
    in_2: List[float] = Field(description="diff parameters", label="paramdiff")
    in_3: bool = Field(
        description="Applies difference (true) or factor (false)", label="diff_or_fact"
    )


class OutputsSchema(BaseModel):
    out_1: PositiveInt = Field(
        description="dimension index that was modified", label="i"
    )
    out_2: List[float] = Field(description="increased parameter", label="paramtestplus")
    out_3: List[float] = Field(
        description="decreased parameter", label="paramtestminus"
    )

    out_4: AnyUrl = Field(
        description="link to a file", label="myfile", content="application/pdf"
    )


def fun(paramrefs: List[float], paramdiff: List[float], diff_or_fact: bool):
    pass


class Model(BaseModel):
    users: typing.List[EmailStr]


print(Model(users=["a@asdf.com", ]))

print(Model.schema_json(indent=2))

# print(OutputsSchema.schema())

# print(schema_json_of(Inputs, indent=2))

print("int ->", schema_json_of(int))
# print("bool ->", schema_json_of(bool))
# print("List[float] ->", schema_json_of(List[float]))
