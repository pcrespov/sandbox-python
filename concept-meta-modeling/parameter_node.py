import random
from pydantic import BaseModel, Field, constr, StrictBool, StrictInt, StrictFloat
from typing import Dict, Union
from uuid import UUID


# Node static metadata: describes static features of this node
#  https://github.com/ITISFoundation/osparc-simcore/blob/master/packages/models-library/src/models_library/services.py#L306
# - in iamge: ServiceDockerData: injected in service image labels which is taken from the metadata.yml
# - in catalog API: ServiceMetaData
#       - basically adds access rights
# - in db: ServiceMetaDataAtDB
#




class MetaData(BaseModel):  # --> schema of the node
    key: str
    version: str
    type_: str = Field(..., alias="type")




### IN THE PROJECT:
# kind


NodeID = UUID
VarName = str # validated with is_valid_variable_name
InputTypes = Union[
    StrictBool,
    StrictInt,
    StrictFloat,
    str,
    # Links to something else ... (i.e. pointers)
    # PortLink,
    # SimCoreFileLink,
    # DatCoreFileLink,
    # DownloadLink,
]
OutputTypes = Union[
    StrictBool,
    StrictInt,
    StrictFloat,
    str,
    # Links to something else ... (i.e. pointers)
    # SimCoreFileLink,
    # DatCoreFileLink,
    # DownloadLink,
]


class Node(BaseModel):
    key: str
    version: str
    label: str
    inputs: Dict[VarName, InputTypes]
    output: Dict[VarName, OutputTypes]

    parent: NodeID


# ---------------


parametrization_meta = MetaData()
parametrization_node = Node()




# all these are different implementations of parameter node

# constant paramater
x = 3
print(x)



# iterators ---

# range-parameter
for x in range(start=1, stop=2, step=.5):
    print(x)

# random-uniform parameter
for x in random.uniform(a=1, b=3):
    print(x)

# random-gauss parameter
for x in random.gauss(mu=3.4, sigma=3):
    print(x)


# expression-parameter (expresso-like)
x = eval("2*y")



from ast import parse

# SEE https://stackoverflow.com/questions/36330860/pythonically-check-if-a-variable-name-is-valid
def is_valid_variable_name(name):
    try:
        parse(f'{name} = None')
        return True
    except (SyntaxError, ValueError, TypeError):
        return False

from keyword import iskeyword

def is_valid_variable_name(name):
    return name.isidentifier() and not iskeyword(name)