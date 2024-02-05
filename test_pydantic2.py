from typing import Annotated

from pydantic import BaseModel, ConfigDict, Field, StringConstraints, ValidationError


# https://docs.pydantic.dev/latest/concepts/models/
def test_models():
    class User(BaseModel):
        id: int
        name: str = "Jane Doe"

    user = User(id=123)

    assert user.name == "Jane Doe"
    assert user.model_fields_set == {"id"}

    assert (
        user.model_dump()
    )  # Note that dict(user) will not recursively convert nested models into dicts, but .model_dump() will

    class Group(BaseModel):
        users: list[User]
        leader: User

    # Note that dict(user) will not recursively convert nested models into dicts, but .model_dump() will
    group = Group(users=[User(id=3), User(id=4)], leader=User(id=2))
    assert group.model_dump() == {
        "users": [{"id": 3, "name": "Jane Doe"}, {"id": 4, "name": "Jane Doe"}],
        "leader": {"id": 2, "name": "Jane Doe"},
    }
    assert dict(group) == {
        "users": [User(id=3, name="Jane Doe"), User(id=4, name="Jane Doe")],
        "leader": User(id=2, name="Jane Doe"),
    }

    # By default, models are mutable and field values can be changed through attribute assignment
    user.name = "Foo"
    assert user.name == "Foo"

    # https://docs.pydantic.dev/latest/concepts/models/#model-methods-and-properties
    print(group.model_computed_fields)
    print(group.model_extra)
    print(group.model_fields_set)
    # print(group.model_parametrized_name())
    assert User.model_validate({"id": 123, "name": "James"})

    # https://docs.pydantic.dev/latest/concepts/models/#nested-models

    # https://docs.pydantic.dev/latest/concepts/models/#rebuild-model-schema

    class Foo(BaseModel):
        x: "Bar"

    class Bar(BaseModel):
        pass

    Foo.model_rebuild()
    print(Foo.model_json_schema())

    # https://docs.pydantic.dev/latest/concepts/models/#arbitrary-class-instances
    class CompanyModel(BaseModel):
        model_config = ConfigDict(from_attributes=True)

        id: int
        public_key: Annotated[str, StringConstraints(max_length=20)]
        name: Annotated[str, StringConstraints(max_length=63)]
        domains: list[Annotated[str, StringConstraints(max_length=255)]]

    # https://docs.pydantic.dev/latest/concepts/models/#reserved-names
    # Using aliases
    class MyModel(BaseModel):
        model_config = ConfigDict(from_attributes=True)

        metadata: dict[str, str] = Field(alias="metadata_")

    # The example above works because aliases HAVE PRIORITY OVER FIELD NAMES for field population

    # https://docs.pydantic.dev/latest/concepts/models/#nested-attributes


def test_error_handling():
    # https://docs.pydantic.dev/latest/concepts/models/#error-handling
    class Model(BaseModel):
        list_of_ints: list[int]
        a_float: float

    data = dict(
        list_of_ints=["1", 2, "bad"],
        a_float="not a float",
    )

    try:
        Model(**data)
    except ValidationError as e:
        print(e)
