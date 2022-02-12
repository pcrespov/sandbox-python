import json

from pydantic import BaseConfig, BaseSettings, Field, ValidationError
from pydantic.fields import ModelField


def get_attrs_tree(obj):
    # long version of json.dumps({ k:str(getattr(field,k)) for k in ModelField.__slots__ } )
    tree = {}
    for name in obj.__class__.__slots__:
        value = getattr(obj, name)
        if hasattr(value.__class__, "__slots__"):
            tree[name] = get_attrs_tree(value)
        else:
            tree[name] = f"{value}"

    return tree


def print_defaults(model_cls):
    for field in model_cls.__fields__.values():
        print(field.name, ":", end="")
        try:
            default = field.get_default()
            print(default, type(default))
        except ValidationError as err:
            print(err)

def dumps_model_class(model_cls):
    d = {field.name: get_attrs_tree(field) for field in model_cls.__fields__.values()}
    return json.dumps(d, indent=2)

###########
def eval_default_value():
    return 42


def create_settings_from_env(field: ModelField):
    def _default_factory():
        field_settings_cls = field.type_
        return field_settings_cls()
    return _default_factory

class MyBaseSettings(BaseSettings):

    class Config(BaseConfig):
        case_sensitive = True  # All must be capitalized
        allow_mutation = False
        frozen = True
        validate_all = True

        @classmethod
        def prepare_field(cls, field: ModelField) -> None:
            super().prepare_field(field)

            auto_default_from_env = field.field_info.extra.get(
                "auto_default_from_env", False
            )

            if auto_default_from_env and issubclass(field.type_, MyBaseSettings):

                field.default_factory = create_settings_from_env(field)
                field.default = None
                # Having a default value, makes this field automatically optional
                field.required = False

            if field.default_factory:
                print(json.dumps({field.name: get_attrs_tree(field)}, indent=1))

    @classmethod
    def from_env(cls, **override_fields):
        return cls(**override_fields)


##############################################


class SubSettings(MyBaseSettings):
    VALUE: int
    VALUE_DEFAULT: int = 42


class Settings(MyBaseSettings):
    VALUE: int
    VALUE_DEFAULT: int = Field(default_factory=eval_default_value)

    VALUE_ENV_DEFAULT: SubSettings = Field(auto_default_from_env=True)


def test_it(monkeypatch):
    monkeypatch.setenv("VALUE", "1")

    settings = Settings.from_env()

    print(Settings.schema_json(indent=1))

    assert settings.dict() == {
        "VALUE": 1,
        "VALUE_DEFAULT": 42,
        "VALUE_ENV_DEFAULT": {"VALUE": 1, "VALUE_DEFAULT": 42},
    }
