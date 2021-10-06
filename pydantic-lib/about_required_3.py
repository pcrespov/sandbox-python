from typing import Optional

import jsonschema

from pydantic import BaseModel, Field


class HealthCheck(BaseModel):
    name: Optional[str] = Field(description="Name of the service")
    status: Optional[str]
    api_version: Optional[str]
    version: Optional[str] = Field(None) # NOTE: None default is never added in the schema

    class Config:
        # Taken from https://github.com/samuelcolvin/pydantic/issues/1270#issuecomment-729555558
        # Adding anyOF instead of [int, null] ... makes it compatible with both jsonschema and openapi
        @staticmethod
        def schema_extra(schema, model):
            for prop, value in schema.get("properties", {}).items():
                # retrieve right field from alias or name
                field = [x for x in model.__fields__.values() if x.alias == prop][0]
                if field.allow_none:
                    # only one type e.g. {'type': 'integer'}
                    if "type" in value:
                        value["anyOf"] = [{"type": value.pop("type")}]
                    # only one $ref e.g. from other model
                    elif "$ref" in value:
                        if issubclass(field.type_, BaseModel):
                            # add 'title' in schema to have the exact same behaviour as the rest
                            value["title"] = (
                                field.type_.__config__.title or field.type_.__name__
                            )
                        value["anyOf"] = [{"$ref": value.pop("$ref")}]
                    value["anyOf"].append({"type": "null"})


print(HealthCheck.schema_json(indent=2))




# NOTE: 
# 1. Without special schema_extra override: I can init with None but at the same time, this instance
# does not match the schema generated because the latter does not include null (disable Config.schema_extra to see that)
# 2. None default is actually NOT added in the schema
#
obj = HealthCheck(name=None, status=None, api_version=None, version=None)

jsonschema.validate(instance=obj.dict(), schema=HealthCheck.schema())




assert HealthCheck.schema() == {
    "title": "HealthCheck",
    "type": "object",
    "properties": {
        "name": {
            "title": "Name",
            "description": "Name of the service",
            "anyOf": [{"type": "string"}, {"type": "null"}],
        },
        "status": {"title": "Status", "anyOf": [{"type": "string"}, {"type": "null"}]},
        "api_version": {
            "title": "Api Version",
            "anyOf": [{"type": "string"}, {"type": "null"}],
        },
        "version": {
            "title": "Version",
            "anyOf": [{"type": "string"}, {"type": "null"}],
        },
    },
}