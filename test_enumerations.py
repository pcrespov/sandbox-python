import enum
from enum import Enum, auto, unique
from typing import Any

import pytest
from pydantic import BaseModel, ValidationError, parse_obj_as


class Color1(Enum):
    RED = "RED"
    BLUE = "BLUE"


class Color2(Enum):
    RED = "RED"
    BLUE = "BLUE"


def test_equivalent_enums_are_not_strictly_equal():

    assert Color1 != Color2

    def to_dict(enum_cls: type[Enum]) -> dict[str, Any]:
        return {m.name: m.value for m in enum_cls}

    assert to_dict(Color1) == to_dict(Color2)


class ColorStrAndEnum1(str, Enum):
    RED = "RED"
    BLUE = "BLUE"


class ColorStrAndEnum2(str, Enum):
    RED = "RED"
    BLUE = "BLUE"


def test_equivalent_enums_in_pydantic():
    class Model(BaseModel):
        color: Color1

    model = parse_obj_as(Model, {"color": Color1.RED})
    assert model.color == Color1.RED

    # Can parse from string
    model = parse_obj_as(Model, {"color": "RED"})
    assert model.color == Color1.RED

    # Can NOT parse from equilalent enum
    with pytest.raises(ValidationError):
        parse_obj_as(Model, {"color": Color2.RED})

    #
    # Using str-enums allow you to parse from equivalent enums!
    #

    class ModelStrAndEnum(BaseModel):
        color: ColorStrAndEnum1

    model = parse_obj_as(ModelStrAndEnum, {"color": ColorStrAndEnum1.RED})
    assert model.color == ColorStrAndEnum1.RED

    # Can parse from string
    model = parse_obj_as(ModelStrAndEnum, {"color": "RED"})
    assert model.color == ColorStrAndEnum1.RED

    # Can parse other equivalent str-enum!
    parse_obj_as(ModelStrAndEnum, {"color": ColorStrAndEnum2.RED})

    # Can still NOT parse equilalent enum(-only)
    with pytest.raises(ValidationError):
        parse_obj_as(ModelStrAndEnum, {"color": Color1.RED})

    # And the opposite? NO
    with pytest.raises(ValidationError):
        parse_obj_as(Color1, {"color": ColorStrAndEnum1.RED})

    with pytest.raises(ValidationError):
        parse_obj_as(Color1, {"color": ColorStrAndEnum2.RED})


def test_inherits_from_str_and_enum():
    @unique
    class SomeEnum(enum.Enum):
        REGISTRATION = "REGISTRATION"
        INVITATION = "INVITATION"

    @unique
    class SomeStrAndEnum(str, enum.Enum):
        REGISTRATION = "REGISTRATION"
        INVITATION = "INVITATION"

    # here are the differences
    assert f"{SomeEnum.REGISTRATION}" == "SomeEnum.REGISTRATION"
    assert f"{SomeStrAndEnum.REGISTRATION}" == "REGISTRATION"

    assert SomeEnum.REGISTRATION != "REGISTRATION"
    assert SomeStrAndEnum.REGISTRATION == "REGISTRATION"

    assert SomeEnum.REGISTRATION != SomeStrAndEnum.REGISTRATION

    # here are the analogies
    assert SomeEnum.REGISTRATION.name == "REGISTRATION"
    assert SomeStrAndEnum.REGISTRATION.name == "REGISTRATION"

    assert SomeEnum.REGISTRATION.value == "REGISTRATION"
    assert SomeStrAndEnum.REGISTRATION.value == "REGISTRATION"


def test_autoname():
    class AutoName(str, Enum):
        def _generate_next_value_(name, start, count, last_values):
            return name

    class Ordinal(AutoName):
        NORTH = auto()
        SOUTH = auto()
        EAST = auto()
        WEST = auto()

    assert list(f"{n}" for n in Ordinal) == [
        "NORTH",
        "SOUTH",
        "EAST",
        "WEST",
    ]

    assert f"{Ordinal.NORTH}" == "NORTH"
    assert Ordinal.NORTH == "NORTH"
    assert Ordinal.NORTH.value == "NORTH"
    assert Ordinal.NORTH.name == "NORTH"


def test_enum_members():
    @unique
    class RunningState(str, Enum):
        """State of execution of a project's computational workflow

        SEE StateType for task state
        """

        UNKNOWN = "UNKNOWN"
        PUBLISHED = "PUBLISHED"
        NOT_STARTED = "NOT_STARTED"
        PENDING = "PENDING"
        STARTED = "STARTED"
        RETRY = "RETRY"
        SUCCESS = "SUCCESS"
        FAILED = "FAILED"
        ABORTED = "ABORTED"

        @property
        def is_running(self) -> bool:
            return self in (
                RunningState.PUBLISHED,
                RunningState.PENDING,
                RunningState.STARTED,
                RunningState.RETRY,
            )

    assert not RunningState.UNKNOWN.is_running
    assert RunningState.PUBLISHED.is_running
