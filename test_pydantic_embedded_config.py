from copy import deepcopy
from typing import Annotated, Any

import pytest
from pydantic.v1 import BaseModel, Field, ValidationError, create_model


def apply_config_recursively(
    cls: type[BaseModel], config_overrides: dict[str, Any]
) -> type[BaseModel]:
    class NewConfig(cls.Config):
        pass

    for key, value in config_overrides.items():
        setattr(NewConfig, key, value)

    new_fields = {}

    # Apply the function recursively to fields that are BaseModel
    for field_name, model_field in cls.__fields__.items():

        if isinstance(model_field.type_, type) and issubclass(
            model_field.type_, BaseModel
        ):
            new_field_type = apply_config_recursively(
                model_field.type_, config_overrides
            )
            new_fields[field_name] = (
                new_field_type,
                deepcopy(model_field.field_info),
            )
        else:
            new_fields[field_name] = (
                model_field.type_,
                deepcopy(model_field.field_info),
            )

    # Create a new model dynamically
    return create_model(f"{cls.__name__}Api", **new_fields, __config__=NewConfig)


def to_camel(string: str) -> str:
    return "".join(
        word.capitalize() if i != 0 else word
        for i, word in enumerate(string.split("_"))
    )


# Define the embedded model
class Address(BaseModel):
    street: str
    city: str
    postal_code: str


# Define the main model
class User(BaseModel):
    first_name: str
    last_name: str
    age: int
    address: Annotated[Address, Field(..., description="some description")]


#
# Should be equivalent to this
#
# class AddressApi(Address):
#     class Config:
#         alias_generator = to_camel
#         allow_population_by_field_name = True
#
#
# class UserApi1(User):
#     address: AddressApi
#
#     class Config:
#         alias_generator = to_camel
#         allow_population_by_field_name = True


UserApi = apply_config_recursively(
    User, {"alias_generator": to_camel, "allow_population_by_field_name": True}
)


def test_it():
    # Example usage
    user_data = {
        "firstName": "John",
        "lastName": "Doe",
        "age": 30,
        "address": {"street": "123 Main St", "city": "Anytown", "postalCode": "12345"},
    }

    with pytest.raises(ValidationError):
        User(**user_data)

    #  alias_generator = to_camel
    user = UserApi(**user_data)
    print(user)

    # user
    print(user.json(by_alias=True, indent=2))
    assert user.dict(by_alias=True) == {
        "firstName": "John",
        "lastName": "Doe",
        "age": 30,
        "address": {"street": "123 Main St", "city": "Anytown", "postalCode": "12345"},
    }

    # user schema
    print(user.schema_json(indent=2))
    assert user.schema()["definitions"]["AddressApi"] == {  # by_alias=True by default
        "title": "AddressApi",
        "type": "object",
        "properties": {
            "street": {"title": "Street", "type": "string"},
            "city": {"title": "City", "type": "string"},
            "postalCode": {"title": "Postalcode", "type": "string"},  # <-- camel case
        },
        "required": ["street", "city", "postalCode"],
    }

    #  allow_population_by_field_name = True
    user2 = UserApi(**user.dict(by_alias=False))
    assert user2 == user
