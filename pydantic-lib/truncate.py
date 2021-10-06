from pydantic import BaseModel


class User(BaseModel):
    id: int
    age: int
    name: str = "John Doe"


class UserExt(User):
    address: str


if __name__ == "__main__":

    extuser = UserExt(id=123, age=32, address="newyork Avenue")

    truncated_user1 = extuser.copy(exclude={"address"})
    print(truncated_user1)

    truncated_user2 = User(extra_to_be_truncated=22, **extuser.dict())
    print(truncated_user2)

    assert truncated_user2 == truncated_user1
    # import pdb; pdb.set_trace()
    # print(extuser.copy(include=User.__fields__))
