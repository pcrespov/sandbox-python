from functools import wraps
from pathlib import Path
from typing import Any, Callable, Dict, Tuple

from pydantic import Field, PositiveInt, validate_arguments
from pydantic.decorator import ValidatedFunction
from pydantic.fields import ModelField
from pydantic.schema import field_schema

from ..services import LATEST_INTEGRATION_VERSION, ServiceDockerData, ServiceType
from ._utils import FRONTEND_SERVICE_KEY_PREFIX, get_fake_thumbnail, register

ModelFieldDict = Dict[str, Any]

def infer_io_from_signature(vd: ValidatedFunction) -> Tuple[ModelFieldDict, ModelFieldDict]:
    # TODO: PC: see notes in sandbox


    # TODO: we take advantage of introspection mechanism of pydantic for the inputs
    # TODO: dummy func for the outputs and validator ??
    # vd.raw_function = function
    # vd.arg_mapping: Dict[int, str] = {}
    # vd.positional_only_args = set()
    # vd.v_args_name = 'args'
    # vd.v_kwargs_name = 'kwargs'
    assert vd.raw_function # nosec
    assert vd.model # nosec


    #

    inputs = {}
    outputs = {}

    for field in vd.model.__fields__.values():
        f_schema, f_definitions, f_nested_models = field_schema(field, model_name_map = {})

    return inputs, outputs


def backend_service(**meta_info):
    """
        meta_info correspond to all fields in ServiceDockerData
    """
    # if not set, create these
    meta_info.setdefault("integration-version", LATEST_INTEGRATION_VERSION)
    meta_info.setdefault("thumbnail", get_fake_thumbnail(meta_info.get("name", "")[:5]))

    def _decorator_function(func: Callable):

        # adds validation when function is called
        @validate_arguments
        @wraps
        def _wrapper_function(*args, **kwargs):
            results = func(*args, **kwargs)
            return results


        # infer meta i/o from function arguments
        inputs, outputs = infer_io_from_signature(_wrapper_function.vd)


        # create meta
        meta = ServiceDockerData.parse_obj(
            {"inputs": inputs, "outputs": outputs, **meta_info}
        )


        # inject meta
        _wrapper_function.meta = meta


        return _wrapper_function

    return _decorator_function




@backend_service(
    key=f"{FRONTEND_SERVICE_KEY_PREFIX}/computational/pyfixture-sleeper",
    version="3.0.0",
    description="A service which awaits for time to pass, two times.",
)
def pyfixture_sleeper(
    input_1: Path = Field(
        ...,
        description="Pick a file containing only one integer",
        title="File with int number",
    ),
    input_2: PositiveInt = Field(
        2,
        description="Choose an amount of time to sleep",
        title="Sleep interval",
        unit="second",
    ),
    input_3: bool = Field(
        False,
        description="If set to true will cause service to fail after it sleeps",
        title="Fail after sleep",
    ),
    input_4: int = Field(
        0,
        description="It will first walk the distance to bed",
        title="Distance to bed",
        unit="meter",
    ),
):
    """ Sleeper 3.0


    """
    from random import randint
    from time import sleep

    sleep(input_2)


    return randint
