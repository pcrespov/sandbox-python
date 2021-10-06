from typing import Optional, Union, Dict
from pydantic import BaseModel, Field
from copy import deepcopy


# SEE https://github.com/samuelcolvin/pydantic/issues/1270
from pydantic import Field

from typing import Optional, Union

class FooModel(BaseModel):
    foo: str


class BarModel(BaseModel):
    bar: str


class YourModel(BaseModel):
    int_foo: int
    str_foo: str
    model_foo: FooModel
    opt_str_foo: Optional[str] = Field(alias='opt_str_foo_alias')
    opt_model_foo: Optional[FooModel]
    union_foo: Union[int, str]
    union_model_foo_str: Union[FooModel, str]
    union_model_foo_bar: Union[FooModel, BarModel]
    opt_union_foo: Union[int, str] = None
    opt_union_foo2: Optional[Union[int, str]]
    opt_union_model_foo_bar: Optional[Union[FooModel, BarModel]]

assert YourModel.schema() == {
    'type': 'object',
    'title': 'YourModel',
    'properties': {
        'int_foo': {
          'title': 'Int Foo',
          'type': 'integer',
        },
        'str_foo': {
            'title': 'Str Foo',
            'type': 'string',
        },
        'model_foo': {'$ref': '#/definitions/FooModel'},
        'opt_str_foo_alias': {
            'title': 'Opt Str Foo Alias',
            'anyOf': [{'type': 'string'}, {'type': 'null'}],
        },
        'opt_model_foo': {
            'title': 'FooModel',
            'anyOf': [{'$ref': '#/definitions/FooModel'}, {'type': 'null'}]
        },
        'union_foo': {
            'title': 'Union Foo',
            'anyOf': [{'type': 'integer'}, {'type': 'string'}],
        },
        'union_model_foo_str': {
            'title': 'Union Model Foo Str',
            'anyOf': [{'$ref': '#/definitions/FooModel'}, {'type': 'string'}],
        },
        'union_model_foo_bar': {
            'title': 'Union Model Foo Bar',
            'anyOf': [{'$ref': '#/definitions/FooModel'}, {'$ref': '#/definitions/BarModel'}],
        },
        'opt_union_foo': {
            'title': 'Opt Union Foo',
            'anyOf': [{'type': 'integer'}, {'type': 'string'}, {'type': 'null'}],
        },
        'opt_union_foo2': {
            'title': 'Opt Union Foo2',
            'anyOf': [{'type': 'integer'}, {'type': 'string'}, {'type': 'null'}],
        },
        'opt_union_model_foo_bar': {
            'title': 'Opt Union Model Foo Bar',
            'anyOf': [{'$ref': '#/definitions/FooModel'}, {'$ref': '#/definitions/BarModel'}, {'type': 'null'}],
        },
    },
    'required': ['int_foo', 'str_foo', 'model_foo', 'union_foo', 'union_model_foo_str', 'union_model_foo_bar'],
    'definitions': {
        'FooModel': {
            'title': 'FooModel',
            'type': 'object',
            'properties': {
                'foo': {'title': 'Foo', 'type': 'string'}
            },
            'required': ['foo']
        },
        'BarModel': {
            'title': 'BarModel',
            'type': 'object',
            'properties': {
                'bar': {'title': 'Bar', 'type': 'string'}
            },
            'required': ['bar']
        }
    }
}


class User(BaseModel):
    name: str
    surname: Optional[str] = "default"
    address: Union[str, None]
    address2: Optional[str]
    #
    # 

    
    class Config:
        # pylint: disable=no-self-argument
        def schema_extra(schema: Dict, _model: "User"):
            # pylint: disable=unsubscriptable-object

            # Patch to allow jsonschema nullable
            # SEE https://github.com/samuelcolvin/pydantic/issues/990#issuecomment-645961530
            pydantic_schema = deepcopy(schema["properties"]["address2"])
            schema["properties"]["address2"] = {
                "anyOf": [{"type": "null"}, pydantic_schema]
            }

            #
            #"type": [
            #    "string",
            #    "null"
            #  ],


print(User.schema_json(indent=2))
