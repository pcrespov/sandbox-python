import inspect
import json
import logging
import os
from pathlib import Path
from typing import Callable, Optional

import typer

# user functions --------------------
#
#  - Preferably some noun
#  - this script needs to be in .osparc/{service}/ folder
#  - this script is
#
#
from myfuncs import cook, hola, salute
from pydantic import BaseModel, BaseSettings, ValidationError, validator
from pydantic.decorator import ValidatedFunction

EXPOSED_REGISTRY = [salute, hola, cook]

# --------------------
# osparc-integration side
#


log = logging.getLogger(__name__)


#
# Expected settings by sidecar
#


class Settings(BaseSettings):
    # envs setup by sidecar
    INPUT_FOLDER: Path
    OUTPUT_FOLDER: Path
    LOG_FOLDER: Optional[Path] = None

    SC_BUILD_TARGET: Optional[str] = None
    SC_COMP_SERVICES_SCHEDULED_AS: Optional[str] = None
    SC_USER_ID: Optional[int] = None
    SC_USER_NAME: Optional[str] = None

    SIMCORE_MEMORY_BYTES_LIMIT: Optional[int] = None
    SIMCORE_NANO_CPUS_LIMIT: Optional[int] = None

    @validator("INPUT_FOLDER", "OUTPUT_FOLDER")
    def check_dir_existance(cls, v):
        if v is None or not v.exists():
            raise ValueError(
                f"Folder {v} does not exists."
                "Expected predefined and created by sidecar"
            )
        return v

    @validator("INPUT_FOLDER")
    def check_input_dir(cls, v):
        f = v / "inputs.json" if v else None
        if f is None or not f.exists():
            raise ValueError(
                f"File {f} does not exists."
                "Expected predefined and created by sidecar"
            )
        return v

    @validator("OUTPUT_FOLDER")
    def check_output_dir(cls, v: Path):
        if not os.access(v, os.W_OK):
            raise ValueError(f"Do not have write access to {v}: {v.stat()}")
        return v

    @property
    def input_file(self) -> Path:
        return self.INPUT_FOLDER / "inputs.json"

    @property
    def output_file(self) -> Path:
        return self.OUTPUT_FOLDER / "outputs.json"


def echo_dot_osparc(core_func: Callable):
    print(f".osparc/{core_func.__name__}/metadata.yaml created")


def echo_jsonschema(core_func: Callable):
    vfunc = ValidatedFunction(function=core_func, config=None)
    print("json-schema for the inputs of {core_func.__name__}")
    print(vfunc.model.schema_json(indent=1))


def run_service(core_func: Callable):
    # TODO: App class? with workflow embedded? split setup + run

    vfunc = ValidatedFunction(function=core_func, config=None)

    # envs and inputs (setup by sidecar)
    try:
        settings = Settings()  # captures  settings TODO: move
        log.info("Settings setup by sidecar %s", settings.json(indent=1))

        inputs: BaseModel = vfunc.model.parse_file(settings.input_file)

    except json.JSONDecodeError as err:
        raise ValueError(
            f"Invalid input file ({settings.input_file}) json format: {err}"
        ) from err

    except ValidationError as err:
        raise ValueError(f"Invalid inputs for {core_func.__name__}: {err}") from err

    # executes
    returned_values = vfunc.execute(inputs)

    # outputs (expected by sidecar)
    # TODO: verify outputs match with expected?
    # TODO: sync name
    if not isinstance(returned_values, tuple):
        returned_values = (returned_values,)

    outputs = {
        f"out_{index}": value for index, value in enumerate(returned_values, start=1)
    }
    settings.output_file.write_text(json.dumps(outputs))


def create_service_cli(core_func: Callable):
    def cli_command(jsonschema_inputs: bool = False, dot_osparc_config: bool = False):

        # TOOLING
        if jsonschema_inputs:
            echo_jsonschema(core_func)
            return

        # TOOLING
        elif dot_osparc_config:
            echo_dot_osparc(core_func)
            return

        # RUN
        run_service(core_func)

    cli_command.__doc__ = (
        f"{core_func.__doc__}\nRuns {core_func.__name__} or produces configs for osparc"
    )
    return cli_command


def __create_service_cli(core_func: Callable):
    # NOTE: do not functools.wrap runner since the CLI exposes the runner and NOT the core_func
    def runner():
        #
        # Knows about function
        # Knows about osparc sidecar passing inputs via json (osparc integration)
        #
        signature = inspect.signature(core_func)

        # INPUTS
        inputs_names = [n for n in signature.parameters.keys()]
        print(f"Expecting {inputs_names} in 'inputs.json'")
        print(
            "Validates 'inputs.json' against func declared inputs (which are also defined in the meta)"
        )
        inputs = {n: None for n in inputs_names}

        # EXECUTION
        print(f"Executing '{core_func.__name__}(**inputs)'")
        print(f"Expecting {signature.return_annotation}")
        outputs = core_func(**inputs)
        print(f"Executed '{core_func.__name__}(**inputs)'")

        # OUTPUTS
        print(f"Got {outputs=}")
        print(f"Validating {signature.return_annotation}")
        print("Writes 'outputs.json'")

    return runner


def create_typer(core_func: Callable):
    app = typer.Typer(help=core_func.__doc__)

    @app.command()
    def run():
        """runs service"""
        run_service(core_func)

    @app.command()
    def config(jsonschema_inputs: bool = False, dot_osparc_config: bool = False):
        """echos configurations"""
        # TOOLING
        if jsonschema_inputs:
            echo_jsonschema(core_func)
            return

        # TOOLING
        elif dot_osparc_config:
            echo_dot_osparc(core_func)
            return

    return app


def create_cli(expose: list[Callable]) -> typer.Typer:
    #
    # Knows that CLI is used w/o arguments/options (osparc integration)
    #
    main = typer.Typer()
    # for func in expose:
    #    app.command(name=func.__name__)(create_service_cli(func))

    for func in expose:
        main.add_typer(create_typer(func), name=func.__name__)

    return main


app = create_cli(expose=EXPOSED_REGISTRY)

if __name__ == "__main__":
    app()
