from pydantic import BaseModel, constr, validator, version
from uuid import UUID, uuid3, NAMESPACE_DNS

from pydantic import ValidationError


class MyModel(BaseModel):
    name: str
    version: constr(regex=r"\d\.\d\.\d")
    id: UUID

    @validator("id", pre=True)
    @classmethod
    def generate_id(cls, v, values):
        # ONLY valid values arrive here
        assert "name" in values
        assert "version" in values
        return uuid3(NAMESPACE_DNS, values["name"] + values["version"])


print("-"*100)

try:
    assert not MyModel(name="fails", version="wrong-format", id=None)
except ValidationError as err:
    print("I expected", err)
    for e in err.errors():
        print(e["loc"])
        print(e["msg"])
        print(e["type"])
        print(e.get("ctx"))


print("-"*100)
obj = MyModel(name="good", version="1.0.0", id=None)
print(obj.schema_json(indent=2))
print(obj.json(indent=2))