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


def salute(*, name: str, lastname: str, formal: bool = False) -> int:
    "Some doc about salute"
    if formal:
        print(f"Hello Mr. {name} {lastname}.")
        return 1
    else:
        print(f"Hello {name} {lastname}")
        return 1


class Cake(BaseModel):
    radius: float = Field(units="cm")
    weight: float = Field(units="kg")


def cook(*, number_of_cakes: int = 1) -> list[Cake]:
    """Esra's cook function"""
    return [Cake(radius=1 + n, weight=0.5) for n in range(number_of_cakes)]
