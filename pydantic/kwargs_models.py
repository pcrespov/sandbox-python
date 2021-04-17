from pydantic import BaseModel
from typing import Union, Dict, List
from uuid import UUID, uuid4
from fastapi import FastAPI

import json
from typing import TypeVar

from pydantic.generics import GenericModel
from typing import Generic


class File(BaseModel):
    filename: str
    id: UUID


DataT = TypeVar("DataT")


class Quantity(GenericModel, Generic[DataT]):
    value: DataT  # some data type the units refers to
    unit: str


class JobInputsMeta:
    pass



InputValueType = Union[File, int, float, int, str, None] # FIXME: all ints and bools will be floats

InputKeywordArgs = Dict[str, InputValueType]
InputArguments = List[InputValueType]



class JobInputs(BaseModel):
    __root__: InputKeywordArgs

    class Config:
        schema_extra = {
            "example": {
                "x": 4.33,
                "n": 55,
                "title": "Temperature",
                "enabled": True,
                "input_file": File(
                    filename="input.txt", id="0a3b2c56-dbcd-4871-b93b-d454b7883f9f"
                ),  # this is a reference to something that exists somewhere else
            }
        }


# print(JobInputs.schema_json(indent=2))


job_inputs = JobInputs.parse_obj(JobInputs.Config.schema_extra["example"])
print(job_inputs)
import pdb; pdb.set_trace()
app = FastAPI()


@app.post("solvers/{solver_id}/jobs", response_model=JobInputs)
def run_job(solver_id: UUID, inputs: JobInputs):
    pass


print(json.dumps(app.openapi(), indent=2))
