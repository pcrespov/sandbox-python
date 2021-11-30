from pydantic import BaseModel,StrictBool, StrictInt, StrictFloat
from typing import List, Union, Dict

BuiltinTypes = Union[StrictBool, StrictInt, StrictFloat, str]


class Input(BaseModel):
    name: str
    schema: BuiltinTypes



class Node(BaseModel):
    """ describes a node """
    name: str
    inputs: Dict[str, BuiltinTypes] = {}



pipeline = [Node(name="g"), Node(name="f", inputs={"x": 3, "y": })]



def create_function(node: Node):
    pass






