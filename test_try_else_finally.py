from multiprocessing.sharedctypes import Value
from random import random


def foo(fail):
    try:
        if fail == 1:
            raise ValueError
        if fail == 2:
            raise RuntimeError
        # return "ok" -> overrides 'else'

    except RuntimeError:
        return "RuntimeError"
    else:
        return "else"
    finally:
        return "finally"  #  -> THIS overrides EVERYTHING


def test_finally_overrides():

    assert foo(1) == "finally"  # ValueError
    assert foo(2) == "finally"  # Runtime
    assert foo(3) == "finally"  # else
