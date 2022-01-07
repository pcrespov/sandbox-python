from pydantic import BaseModel
from pydantic_models_factory import copy_model
from pydantic import create_model
from typing import Dict


class Node(BaseModel):
    key: str
    version: str


class ProjectWithType(BaseModel):
    nodes: Node


class ProjectWithDict(BaseModel):
    nodes: Dict[str, Node]


ProjectDynamic = create_model("ProjectDynamic", workbench=(Dict[str, Node], ...))


print(ProjectWithType.schema_json(indent=1))
print(ProjectWithDict.schema_json(indent=1))


_ProjectClone = copy_model(Project, name="ProjectClone")

print(_ProjectClone(workbench={}).json(indent=2))
