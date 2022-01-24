"""
Implements a model for CWL specs that fits tutorial

https://www.commonwl.org/user_guide/

"""

import textwrap
from pathlib import Path
from typing import Any, Dict, List, Optional, Union

import pytest
import yaml
from pydantic import BaseModel, Field, PositiveInt, constr


def snake_to_camel(subject):
    parts = subject.lower().split("_")
    return parts[0] + "".join(x.title() for x in parts[1:])


# matches a variable name
VarName = constr(regex=r"\S", strip_whitespace=True)
SHA1Str = constr(regex=r"^sha1\$([a-fA-F0-9]{40})$")


class BaseCWLModel(BaseModel):
    class Config:
        alias_generator = snake_to_camel


class InputBinding(BaseCWLModel):
    position: Optional[PositiveInt] = None
    prefix: Optional[str] = None
    separate: bool = Field(
        True,
        description="When the option separate is false (the default value is true),"
        " the prefix and value are combined into a single argument e.g. '-i 42' is rendered as '-i42'.",
    )


class OutputBinding(BaseCWLModel):
    glob: str = Field(..., description="glob match")


class CWLInput(BaseCWLModel):
    type: str = Field(
        ...,
        description="When the parameter type ends with a question mark ? it indicates that the parameter is optional.",
    )
    input_binding: InputBinding

    @property
    def optional(self):
        return self.type.endswith("?")


class CWLOutput(BaseCWLModel):
    type: str = Field(
        ...,
        description="When the parameter type ends with a question mark ? it indicates that the parameter is optional.",
    )
    output_binding: OutputBinding


class OutputObject(BaseModel):
    location: str
    basename: str
    cwl_class: str = Field(..., alias="class") # TODO: pydantic literals or enum?
    checksum: SHA1Str
    size: int = 0
    path: Path

    class Config:
        schema_extra = {
            "examples": [
                {
                    "location": "file:///home/me/cwl/user_guide/hello.txt",
                    "basename": "hello.txt",
                    "class": "File",
                    "checksum": "sha1$da39a3ee5e6b4b0d3255bfef95601890afd80709",
                    "size": 0,
                    "path": "/home/me/cwl/user_guide/hello.txt",
                }
            ]
        }


class CWLNode(BaseCWLModel):
    cwl_version: str
    cwl_class: str = Field(..., alias="class")
    base_command: Union[str, List[str]]
    inputs: Dict[VarName, CWLInput]
    outputs: Optional[Dict[VarName, CWLOutput]] = None  # nullable!


# --------------------------------------------------------


def test_example_1():
    # https://www.commonwl.org/user_guide/02-1st-example/index.html
    CWL_CONTENT = textwrap.dedent(
        """\
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
    """
    )

    data = yaml.safe_load(CWL_CONTENT)
    model = CWLNode.parse_obj(data)

    print(model.json(indent=2))


def test_example_2():
    # https://www.commonwl.org/user_guide/03-input/index.html
    CWL_CONTENT = textwrap.dedent(
        """ #!/usr/bin/env cwl-runner
        cwlVersion: v1.0
        class: CommandLineTool
        baseCommand: echo
        inputs:
            example_flag:
                type: boolean
                inputBinding:
                    position: 1
                    prefix: -f
            example_string:
                type: string
                inputBinding:
                    position: 3
                    prefix: --example-string
            example_int:
                type: int
                inputBinding:
                    position: 2
                    prefix: -i
                    separate: false
            example_file:
                type: File?
                inputBinding:
                    prefix: --file=
                    separate: false
                    position: 4
        outputs: []
        """
    )

    data = yaml.safe_load(CWL_CONTENT)
    model = CWLNode.parse_obj(data)

    print(model.json(indent=2))

    assert model.inputs["example_file"].optional


def test_example_returning_output_files():
    ## https://www.commonwl.org/user_guide/04-output/index.html
    CWL_CONTENT = textwrap.dedent(
        """
        #!/usr/bin/env cwl-runner

        cwlVersion: v1.0
        class: CommandLineTool
        baseCommand: [tar, --extract]
        inputs:
            tarfile:
                type: File
                inputBinding:
                    prefix: --file
        outputs:
            example_out:
                type: File
                outputBinding:
                    glob: hello.txt
        """
    )

    data = yaml.safe_load(CWL_CONTENT)
    model = CWLNode.parse_obj(data)

    print(model.json(indent=2))

    assert not model.inputs["tarfile"].optional

    for obj in OutputObject.Config.schema_extra["examples"]:
        output = OutputObject.parse_obj(obj)
