# Adapted from https://github.com/samuelcolvin/pydantic/issues/1270#issuecomment-729298342

from pydantic import BaseModel, Field
from typing import Optional


class YourModel(BaseModel):
    required_foo: int
    nullable_bar: Optional[str] = Field(alias="alias_nullable_bar")
    nullable_other: Optional[int]

    class Config:
        @staticmethod
        def schema_extra(schema, model):
            for prop, value in schema.get("properties", {}).items():
                if prop in [
                    "alias_nullable_bar",
                    "nullable_other",
                ]:  # Your actual nullable fields go in this list.
                    was = value["type"]
                    value["type"] = [was, "null"]


print(YourModel.schema_json(indent=2))


assert YourModel.schema() == {
    "title": "YourModel",
    "type": "object",
    "properties": {
        "required_foo": {"title": "Required Foo", "type": "integer"},
        "alias_nullable_bar": {
            "title": "Alias Nullable Bar",
            "type": ["string", "null"],
        },
        "nullable_other": {"title": "Nullable Other", "type": ["integer", "null"]},
    },
    "required": ["required_foo"],
}
