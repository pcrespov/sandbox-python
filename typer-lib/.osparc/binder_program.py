import importlib
import importlib.machinery
import importlib.util
import inspect
import json
import logging
import os
import sys
from copy import deepcopy
from inspect import Parameter, Signature
from pathlib import Path
from textwrap import indent
from typing import Any, Callable, Final, Mapping, Optional, get_args, get_origin

import typer
import yaml
from pydantic import (
    BaseModel,
    BaseSettings,
    EmailStr,
    ValidationError,
    constr,
    validate_arguments,
    validator,
)
from pydantic.decorator import ValidatedFunction
from pydantic.tools import schema_of

log = logging.getLogger(__name__)


# user functions --------------------
#
#  - Preferably some noun
#  - this script needs to be in .osparc/{service}/ folder
#  - this script is
#


DOT_OSPARC_DIR = (
    Path(sys.argv[0] if __name__ == "__main__" else __file__).resolve().parent
)
assert DOT_OSPARC_DIR.name == ".osparc", "Should always be under .osparc/"

SETTINGS = json.loads((DOT_OSPARC_DIR / "settings.json").read_text())


def _import_module_from_path(module_name: str, module_path: Path):
    # SEE https://docs.python.org/3/library/importlib.html#importing-a-source-file-directly

    spec = importlib.util.spec_from_file_location(module_name, module_path)
    assert spec
    module = importlib.util.module_from_spec(spec)

    assert module
    assert spec.loader
    sys.modules[module_name] = module
    spec.loader.exec_module(module)

    # filefinder = importlib.machinery.FileFinder(f"{CURRENT_DIR.parent}")
    # spec1 = filefinder.find_spec(module_name)


def discover_published_functions() -> list:

    published = []

    # publish_functions
    # TODO: with pydantic
    functions_dotted_names = SETTINGS["publish_functions"]
    for dotted_name in functions_dotted_names:
        parts = dotted_name.split(".")
        module_name = ".".join(parts[:-1])
        func_name = parts[-1]

        try:
            try:
                module = importlib.import_module(module_name)
            except (ImportError, ModuleNotFoundError):
                # assumes code in $here, given $here/.osparc
                module_tail_path = "/".join(parts[:-1]) + ".py"
                module = _import_module_from_path(
                    module_name, DOT_OSPARC_DIR.parent / module_tail_path
                )
            func = getattr(module, func_name)
            published.append(func)
        except (AttributeError, ModuleNotFoundError, FileNotFoundError) as err:
            log.error(
                "Skipping publish_functions %s %s:\n%s",
                dotted_name,
                "Could not module. TIP: Include path to the package in PYTHONPATH environment variable",
                indent(f"{err}", prefix=" "),
            )

    return published


# --------------------
# osparc binder program
#
#  runs: creates entrypoint to run function
#      - Creates CLI that
#           - reads environs
#           - load + parse inputs -> model
#           - calls core_func (inputs)
#           - write outputs
#      -
#


#
# Expected settings by sidecar
#


#
# Needed for execution
#
class ContainerEnvironmentSettings(BaseSettings):
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
    def check_dir_exists(cls, v):
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


class Author(BaseModel):
    name: str
    email: EmailStr
    affiliation: str


# SE# https://semver.org/#is-there-a-suggested-regular-expression-regex-to-check-a-semver-string
# SEE https://regex101.com/r/Ly7O1x/3/
SEMANTIC_VERSION_RE1 = r"^(?P<major>0|[1-9]\d*)\.(?P<minor>0|[1-9]\d*)\.(?P<patch>0|[1-9]\d*)(?:-(?P<prerelease>(?:0|[1-9]\d*|\d*[a-zA-Z-][0-9a-zA-Z-]*)(?:\.(?:0|[1-9]\d*|\d*[a-zA-Z-][0-9a-zA-Z-]*))*))?(?:\+(?P<buildmetadata>[0-9a-zA-Z-]+(?:\.[0-9a-zA-Z-]+)*))?$"
# cg1 = major, cg2 = minor, cg3 = patch, cg4 = prerelease and cg5 = buildmetadata
SEMANTIC_VERSION_RE2 = r"^(0|[1-9]\d*)\.(0|[1-9]\d*)\.(0|[1-9]\d*)(?:-((?:0|[1-9]\d*|\d*[a-zA-Z-][0-9a-zA-Z-]*)(?:\.(?:0|[1-9]\d*|\d*[a-zA-Z-][0-9a-zA-Z-]*))*))?(?:\+([0-9a-zA-Z-]+(?:\.[0-9a-zA-Z-]+)*))?$"


class VersionStr(str):
    __root__ = constr(regex=SEMANTIC_VERSION_RE2)


@validate_arguments(config=dict(arbitrary_types_allowed=True))
def echo_dot_osparc(
    core_func: Callable,
    version: VersionStr,
    authors: list[Author],
    contact: Optional[EmailStr] = None,
):
    print(f".osparc/{core_func.__name__}/metadata.yaml created")

    if contact is None:
        contact = authors[0].email

    # FIXME: name and key seem to be the same??!
    _PACKAGE_NAME: Final = "ofs"  # __name__.split(".")[0]
    _TEMPLATE_META: Final = {
        "name": "TO_BE_DEFINED",
        "thumbnail": "https://upload.wikimedia.org/wikipedia/commons/thumb/b/bd/Test.svg/315px-Test.svg.png",
        "description": "",
        "key": "simcore/services/comp/TO_BE_DEFINED",
        "version": version,
        "integration-version": "1.0.0",
        "type": "computational",
        "authors": [a.dict() for a in authors],
        "contact": contact,
        "inputs": {},
        "outputs": {},
    }

    # TODO: class MetaDict(TypedDict):
    #    name: str
    #    thumbnail: str
    #    description: str

    MetaDict = dict[str, Any]

    def _name_type(parameter_annotation):
        try:
            if issubclass(parameter_annotation, float):
                name = "number"
            elif issubclass(parameter_annotation, int):
                name = "integer"
            elif issubclass(parameter_annotation, str):
                name = "string"
            else:
                name = f"{parameter_annotation}".replace("typing.", "")
        except TypeError:
            name = f"{parameter_annotation}".replace("typing.", "")

        return name

    def _replace_value_in_dict(item: Any, original_schema: dict[str, Any]):
        #
        # Taken and adapted from https://github.com/samuelcolvin/pydantic/issues/889#issuecomment-850312496
        # TODO: check https://github.com/gazpachoking/jsonref

        if isinstance(item, list):
            return [_replace_value_in_dict(i, original_schema) for i in item]
        elif isinstance(item, dict):
            if "$ref" in item.keys():
                # Limited to something like "$ref": "#/definitions/Engine"
                definitions = item["$ref"][2:].split("/")
                res = original_schema.copy()
                for definition in definitions:
                    res = res[definition]
                return res
            else:
                return {
                    key: _replace_value_in_dict(i, original_schema)
                    for key, i in item.items()
                }
        else:
            return item

    def _resolve_refs(schema: dict[str, Any]) -> dict[str, Any]:
        if "$ref" in str(schema):
            # NOTE: this is a minimal solution that cannot cope e.g. with
            # the most generic $ref with might be URLs. For that we will be using
            # directly jsonschema python package's resolver in the near future.
            # In the meantime we can live with this
            return _replace_value_in_dict(deepcopy(schema), deepcopy(schema.copy()))
        return schema

    def _create_inputs(parameters: Mapping[str, Parameter]) -> dict[str, Any]:
        inputs = {}
        for parameter in parameters.values():
            # should only allow keyword argument
            assert parameter.kind == parameter.KEYWORD_ONLY
            assert parameter.annotation != Parameter.empty

            # build each input
            description = getattr(
                parameter.annotation,
                "description",
                parameter.name.replace("_", " ").capitalize(),
            )

            # FIXME: files are represented differently!
            content_schema = schema_of(
                parameter.annotation,
                title=parameter.name.capitalize(),
            )

            data = {
                "label": parameter.name,
                "description": description,
                "type": "ref_contentSchema",
                "contentSchema": _resolve_refs(content_schema),
            }

            if parameter.default != Parameter.empty:
                # TODO: what if partial-field defaults?
                data["defaultValue"] = parameter.default

            inputs[parameter.name] = data
        return inputs

    def _as_args_tuple(return_annotation: Any) -> tuple:
        if return_annotation == Signature.empty:
            return tuple()

        origin = get_origin(return_annotation)

        if origin and origin is tuple:
            # multiple outputs
            return_args_types = get_args(return_annotation)
        else:
            # single output
            return_args_types = (return_annotation,)
        return return_args_types

    def _create_outputs(return_annotation: Any) -> dict[str, Any]:
        # TODO: add extra info on outputs?
        outputs = {}

        return_args_types = _as_args_tuple(return_annotation)
        for index, return_type in enumerate(return_args_types, start=1):
            name = f"out_{index}"

            if return_type is None:
                continue

            display_name = f"Out{index} {_name_type(return_type)}"
            content_schema = schema_of(return_type, title=display_name)
            data = {
                "label": display_name,
                "description": "",
                "type": "ref_contentSchema",
                "contentSchema": _resolve_refs(content_schema),
            }
            outputs[name] = data
        return outputs

    def _create_meta(func: Callable) -> MetaDict:

        if inspect.isgeneratorfunction(func):
            raise NotImplementedError(f"Cannot process function iterators as {func}")

        signature = inspect.signature(func)
        inputs = _create_inputs(signature.parameters)
        outputs = _create_outputs(signature.return_annotation)

        service_name = f"{_PACKAGE_NAME}-{func.__name__}"

        meta = deepcopy(_TEMPLATE_META)
        meta["name"] = service_name
        meta["key"] = f"simcore/services/comp/ofs-{func.__name__}"
        meta["inputs"] = inputs
        meta["outputs"] = outputs

        return meta

    print(
        yaml.safe_dump(
            _create_meta(func=core_func), sys.stdout, indent=1, sort_keys=False
        )
    )


def echo_jsonschema(core_func: Callable):
    vfunc = ValidatedFunction(function=core_func, config=None)
    print("json-schema for the inputs of {core_func.__name__}")
    print(vfunc.model.schema_json(indent=1))


def run_service(core_func: Callable):
    # TODO: App class? with workflow embedded? split setup + run

    vfunc = ValidatedFunction(function=core_func, config=None)

    # envs and inputs (setup by sidecar)
    try:
        settings = ContainerEnvironmentSettings()  # captures  settings TODO: move
        log.info("Settings setup by sidecar %s", settings.json(indent=1))

        inputs: BaseModel = vfunc.model.parse_file(settings.input_file)

    except json.JSONDecodeError as err:
        assert settings
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
    def cli_command(
        dot_osparc_config: bool = False,
        version: str = "0.1.0",
        jsonschema_inputs: bool = False,
    ):

        # TOOLING
        if jsonschema_inputs:
            echo_jsonschema(core_func)
            return

        # TOOLING
        elif dot_osparc_config:
            echo_dot_osparc(
                core_func,
                version=version,
                authors=SETTINGS.get("metadata", {}).get("authors", []),
            )
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
    def config(
        dot_osparc_config: bool = False,
        version: str = "0.1.0",
        jsonschema_inputs: bool = False,
    ):
        """echos configurations"""
        # TOOLING
        if jsonschema_inputs:
            echo_jsonschema(core_func)
            return

        # TOOLING
        elif dot_osparc_config:
            echo_dot_osparc(
                core_func,
                version=version,
                authors=SETTINGS.get("metadata", {}).get("authors", []),
            )
            return

    return app


def create_cli(expose: list[Callable]) -> typer.Typer:
    #
    # Knows that CLI is used w/o arguments/options (osparc integration)
    #
    assert expose

    main = typer.Typer()
    # for func in expose:
    #    app.command(name=func.__name__)(create_service_cli(func))

    for func in expose:
        main.add_typer(create_typer(func), name=func.__name__)

    return main


main = create_cli(expose=discover_published_functions())

if __name__ == "__main__":
    main()
