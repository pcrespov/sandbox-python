from pydantic import BaseModel
from pydantic import BaseModel, Field, SecretStr


## https://github.com/samuelcolvin/pydantic/issues/830


def solution_with_view():
    # https://github.com/samuelcolvin/pydantic/issues/830#issuecomment-626688520

    def view(name, include=None, exclude=None):
        def wrapper(cls):
            include_ = set(cls.__fields__.keys())
            if include is not None:
                include_ &= set(include)
            exclude_ = set()
            if exclude is not None:
                exclude_ = set(exclude)
            if include and exclude and set(include) & set(exclude):
                raise ValueError("include and exclude cannot contain the same fields")
            fields = {
                k: v
                for k, v in cls.__fields__.items()
                if k in include_ and k not in exclude_
            }

            class ViewDesc:
                def __get__(self, obj, owner=None):
                    def __init__(self):
                        if obj is not None:
                            kwds = {
                                k: v
                                for k, v in obj.dict().items()
                                if k in include_ and k not in exclude_
                            }
                        else:
                            kwds = {}
                        super(owner, self).__init__(**kwds)

                    view_cls = type(
                        name, (cls,), {"__init__": __init__, "__fields__": fields}
                    )
                    return view_cls

            setattr(cls, name, ViewDesc())
            return cls

        return wrapper

    @view("UserOut", exclude=["password"])
    class User(BaseModel):
        user_id: int
        username: str
        password: str

    user = User(user_id=1, username="root", password="sercret")
    print(user.UserOut())

    #
    # this is useful to create responses with a subset of the model
    # but cannot be used to parse and validate some subsets of User
    #


#
# NEW FEATURE COMING
#
# https://github.com/samuelcolvin/pydantic/pull/2231
#
#
def exclude_in_Field_parameter_1():
    class User(BaseModel):
        id: int
        username: str
        password: SecretStr = Field(..., exclude=True)

    class Transaction(BaseModel):
        id: str
        user: User = Field(
            ..., exclude={"username"}
        )  # # This feature still not released
        value: int

        class Config:
            # this is already supported
            fields = {"value": {"exclude": True}}

    t = Transaction(
        id="1234567890",
        user=User(id=42, username="JohnDoe", password="hashedpassword"),
        value=9876543210,
    )

    print(t.dict())

    # This feature still not released
    assert t.dict() == {"id": "1234567890", "user": {"id": 42}, "value": 9876543210}


def exclude_in_Field_parameter_2():
    class User(BaseModel):
        id: int
        username: str  # overridden by explicit exclude
        password: SecretStr = Field(exclude=True)

    class Transaction(BaseModel):
        id: str
        user: User
        value: int

    t = Transaction(
        id="1234567890",
        user=User(id=42, username="JohnDoe", password="hashedpassword"),
        value=9876543210,
    )

    print(t.dict(exclude={"value": True, "user": {"username"}}))
