import pytest

from typing import NamedTuple


class ExpectedCategories(NamedTuple):
    is_true: bool
    number: int

    def __str__(self) -> str:
        return f"is_true:{self.is_true}, number:{self.number}"


# @pytest.mark.parametrize("x,y", [(1, 2), (3, 2)], ids=["first", "second"])
# def test_it1(x, y):
#     assert x == y


def idfun(e):
    if isinstance(e, ExpectedCategories):
        # gets every element in the tuple, i.e. 1, 2, 3, 2
        return f"{e}"


@pytest.mark.parametrize(
    "x,y",
    [(1, ExpectedCategories(False, 1)), (3, ExpectedCategories(False, 1))],
    ids=idfun,
)
def test_it2(x, y):
    assert x == y.number
