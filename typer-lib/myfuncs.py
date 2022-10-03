from pydantic import BaseModel, Field

# user functions --------------------
#
#  - Preferably some noun
#


def hola() -> None:
    """
    This is some help doc for hello
    """
    print("hello world")


def salute(name: str, lastname: str, formal: bool = False) -> int:
    "Some doc about salute"
    if formal:
        print(f"Hello Mr. {name} {lastname}.")
        return 1
    else:
        print(f"Hello {name} {lastname}")
        return 1


class Cake(BaseModel):
    length: float = Field(units="cm")
    weight: float = Field(units="kg")


def cook(cake: Cake) -> Cake:
    return cake
