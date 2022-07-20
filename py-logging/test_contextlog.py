from contextlib import contextmanager
from xxlimited import foo


@contextmanager
def log_context(msg):
    try:
        ctx = {}
        print("\nSTARTED", msg)

        yield ctx

    finally:
        print("FINISHED with", ctx)


def fail():
    raise RuntimeError


def success():
    return 5


import pytest


def test_it():
    with pytest.raises(RuntimeError):
        with log_context("failing function") as ctx:
            ctx["r"] = r = fail()


def test_it2():
    with log_context("failing function") as ctx:
        ctx["r"] = r = success()


from typing import NamedTuple, Optional


class CommandResult(NamedTuple):
    success: bool
    message: str
    command: str
    elapsed: Optional[float]

    def __repr__(self):
        return "{self.command} [{self.elapsed}s]: {message}"


from pprint import pprint

import string


def test_it3():
    c = CommandResult(
        success=True,
        message="\n".join(string.ascii_letters),
        elapsed=12.3456789,
        command="foo",
    )
    pprint(c)
    print(c)
