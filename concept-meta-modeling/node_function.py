from pydantic import validate_arguments, Field, BaseModel
from pathlib import Path


class ExtPath(Path):
    pass


class Parameter(Field):
    pass


def backend_task():
    pass


from typing import Iterator


from enum import Enum


class MethodType(Enum):
    CUSTOM = 0
    LINESPACE = 1
    RANDOM = 2



def generate_int(method: MethodType, start: int, stop: int, step: int) -> int:
    for i in range(start=start, stop=stop, step=step):
        yield i







# - Register function in catalog
# - weak/strong meta and data validation
# - 
@backend_task(
    "simcore/services/comp/itis/sleeper",
    version="2.1.1",
    description="A service which awaits for time to pass, two times.",
)
def sleeper_func(
    input_1: Path = Parameter(
        ...,
        description="Pick a file containing only one integer",
        title="File with int number",
    ),
    input_2: int = Parameter(
        2,
        description="Choose an amount of time to sleep",
        title="Sleep interval",
        unit="second",
    ),
    input_3: bool = Parameter(
        False,
        description="If set to true will cause service to fail after it sleeps",
        title="Fail after sleep",
    ),
    input_4: int = Parameter(
        0,
        description="It will first walk the distance to bed",
        title="Distance to bed",
        unit="meter",
    ),
):
    pass


# sleeper-meta.yml -> produce callable
def sleeper(**inputs):
    pass
