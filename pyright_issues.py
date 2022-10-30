from enum import Enum
from typing import Union


def foo(x: list[Union[str, int]]):
    ...


def bar(x: list[Union[str, Enum]]):
    ...


x1 = ["one", "two"]
bar(x1)  # <----
# Argument of type "list[str]" cannot be assigned to parameter "x" of type "List[str | Enum]" in function "bar"
#  "list[str]" is incompatible with "List[str | Enum]"
#    TypeVar "_T@list" is invariant
#      Type "str" cannot be assigned to type "str | Enum"
#        "str" is incompatible with "Enum"PylancereportGeneralTypeIssues

x2: list[Union[str, Enum]] = ["one", "two"]
bar(x2)

x3 = ["one", "two"]
foo(x3)  # <---

x4: list[Union[str, int]] = ["one", "two"]
foo(x4)
