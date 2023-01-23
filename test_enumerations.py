import enum
from enum import Enum, auto, unique


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


print(RunningState.UNKNOWN.is_running)
print(RunningState.PUBLISHED.is_running)


class ConfirmationAction(enum.Enum):
    REGISTRATION = "REGISTRATION"
    RESET_PASSWORD = "RESET_PASSWORD"
    CHANGE_EMAIL = "CHANGE_EMAIL"
    INVITATION = "INVITATION"


@unique
class ConfirmationActionNEW(str, enum.Enum):
    REGISTRATION = "REGISTRATION_NEW"
    RESET_PASSWORD = "RESET_PASSWORD"
    CHANGE_EMAIL = "CHANGE_EMAIL"
    INVITATION = "INVITATION"


class UserStatusNEW(str, Enum):
    """
    pending: user registered but not confirmed
    active: user is confirmed and can use the platform
    expired: user is not authorized because it expired after a trial period
    banned: user is not authorized
    """

    CONFIRMATION_PENDING = "PENDING"
    ACTIVE = "ACTIVE"
    EXPIRED = "EXPIRED"
    BANNED = "BANNED"


def test_inherits_from_str_and_enum():

    assert f"{ConfirmationAction.REGISTRATION}" == "ConfirmationAction.REGISTRATION"
    assert ConfirmationAction.REGISTRATION != "REGISTRATION"
    assert ConfirmationAction.REGISTRATION.name == "REGISTRATION"

    assert f"{ConfirmationActionNEW.REGISTRATION}" == "REGISTRATION_NEW"
    assert ConfirmationActionNEW.REGISTRATION == "REGISTRATION_NEW"
    assert ConfirmationActionNEW.REGISTRATION.value == "REGISTRATION_NEW"


class AutoName(str, Enum):
    def _generate_next_value_(name, start, count, last_values):
        return name


class Ordinal(AutoName):
    NORTH = auto()
    SOUTH = auto()
    EAST = auto()
    WEST = auto()


def test_autoname():
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
