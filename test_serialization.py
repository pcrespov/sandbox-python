import json
from datetime import datetime
from uuid import UUID

from pydantic import BaseModel


class CustomEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, BaseModel):
            # Serialize the Pydantic model by converting it to a dictionary
            data = obj.dict()
            data["__type__"] = obj.__class__.__name__
            return data
        return super().default(obj)


class Job(BaseModel):
    id: UUID
    name: str
    inputs_checksum: str
    created_at: datetime


# CAN USE json_encoders to inject  CustomEncoder
# SEE https://docs.pydantic.dev/latest/usage/exporting_models/#json_encoders


def from_json(json_data):
    data = json.loads(json_data)

    if class_name := data.pop("__type__", None):
        # TODO: factory
        if class_name == Job.__name__:
            return Job.parse_obj(data)
        # Add other class types here as needed

    return data  # Return as-is if no class information is present


job = Job.parse_obj(
    {
        "id": "677a4776-d36c-43a2-a989-589a4c583379",
        "name": "solvers/simcore%2Fservices%2Fcomp%2Fitis%2Fsleeper/releases/2.0.2/jobs/677a4776-d36c-43a2-a989-589a4c583379",
        "inputs_checksum": "52bfd4885aa1daf5c16fdd39b9118f652c4977c4021c900794dc125cf123718e",
        "created_at": "2022-06-01T15:28:56.807441",
    }
)
