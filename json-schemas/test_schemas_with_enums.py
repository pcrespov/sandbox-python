from enum import Enum, IntEnum

from pydantic import BaseModel


class StringEnum(str, Enum):
    # Only str
    A = "A"
    B = "B"


class IntegerEnum(IntEnum):
    # Only int
    A = 1
    B = 2


class MixedEnum(Enum):
    # Mixed types
    A = 1
    B = "B"
    C = None


class Data(BaseModel):
    s: StringEnum
    i: IntegerEnum
    m: MixedEnum


def test_it():

    print(Data.schema_json(indent=1))
    print("")

    assert Data.schema() == {
        "title": "Data",
        "type": "object",
        "properties": {
            "s": {"$ref": "#/definitions/StringEnum"},
            "i": {"$ref": "#/definitions/IntegerEnum"},
            "m": {"$ref": "#/definitions/MixedEnum"},
        },
        "required": ["s", "i", "m"],
        "definitions": {
            "StringEnum": {
                "title": "StringEnum",
                "description": "An enumeration.",
                "enum": ["A", "B"],
                "type": "string",  # <--- has a type
            },
            "IntegerEnum": {
                "title": "IntegerEnum",
                "description": "An enumeration.",
                "enum": [1, 2],
                "type": "integer",  # <--- has a type
            },
            "MixedEnum": {
                "title": "MixedEnum",
                "description": "An enumeration.",
                "enum": [1, "B", None],
                # <--- has NO type
            },
        },
    }
