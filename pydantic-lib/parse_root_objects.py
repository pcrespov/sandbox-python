from pydantic import BaseModel, Field, constr, ConstrainedStr
from typing import Dict, Any

# in pydantic < 1.8 we had to add __root__ in embedded root basemodels
#
PortKey: ConstrainedStr = constr(regex="^[-_a-zA-Z0-9]+$")


class Port(BaseModel):
    key: str


class PortsMapping(BaseModel):
    __root__: Dict[PortKey, Port]


class InputsList(PortsMapping):
    pass


class Nodeports(BaseModel):
    internal_inputs: InputsList = Field(..., alias="inputs")
    outputs: Dict[PortKey, Port]

    # def __init__(self, **data: Any):
    #    super().__init__(**data)
    #
    #    ADD post init here
    #


node = Nodeports(
    inputs={
        "in1": {
            "key": "X",
        },
    },
    outputs={"out1": {"key": "Y"}},
)
print(node.json(indent=2))


# https://pydantic-docs.helpmanual.io/usage/models/#custom-root-types
# The root value can be passed to the model __init__ via the __root__ keyword argument, or as the first and only argument to parse_obj.
data = {
        "in1": {
            "key": "X",
        },
    }
inputs=InputsList.parse_obj(data)
print(inputs.json(indent=2))

inputs=InputsList(__root__ =data)
print(inputs.json(indent=2))