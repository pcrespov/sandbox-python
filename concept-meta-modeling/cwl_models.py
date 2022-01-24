import textwrap
from re import L
from typing import Any, Dict, List

import yaml
from pydantic import BaseModel, Field, PositiveInt, constr

#
#  https://www.commonwl.org/user_guide/01-introduction/index.html
# CWL is a way to describe command line tools and connect them together to create workflows. Because CWL is a specification and not a specific piece of software, tools and workflows described using CWL are portable across a variety of platforms that support the CWL standard.
#
#


def snake_to_camel(subject):
    parts = subject.lower().split("_")
    return parts[0] + "".join(x.title() for x in parts[1:])


# matches a variable name
InputName = constr(regex=r"\S", strip_whitespace=True)


class CWLConfig:
    class Config:
        alias_generator = snake_to_camel



class InputBinding(BaseModel, CWLConfig):
    position: PositiveInt


class CWLInput(BaseModel, CWLConfig):
    type: str
    input_binding: InputBinding 


class CWLNode(BaseModel, CWLConfig):
    cwl_version: str
    cwl_class: str = Field(..., alias="class")
    base_command: str
    inputs: Dict[InputName, CWLInput]
    outputs: List[Any]



def test_example_1():
    # https://www.commonwl.org/user_guide/02-1st-example/index.html
    CWL_CONTENT = textwrap.dedent("""\
    #!/usr/bin/env cwl-runner

    cwlVersion: v1.0
    class: CommandLineTool
    baseCommand: echo
    inputs:
    message:
        type: string
        inputBinding:
        position: 1
    outputs: []
    """)

    data = yaml.safe_load(CWL_CONTENT)
    model = CWLNode.parse_obj(data)

    print(model.json(indent=2))
    print("---")
