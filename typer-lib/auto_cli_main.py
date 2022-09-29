import inspect
from typing import Callable

import typer

# user functions --------------------


def hello() -> None:
    """
    This is some help doc for hello
    """
    print("hello world")


def salute(name: str, lastname: str, formal: bool = False) -> int:
    "Some doc about salute"
    if formal:
        print(f"Good day Ms. {name} {lastname}.")
        return 1
    else:
        print(f"Hello {name} {lastname}")
        return 1


# --------------------
# osparc-integration side
#


def create_service_cli(core_func: Callable):
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


def create_cli(expose: list[Callable]) -> typer.Typer:
    #
    # Knows that CLI is used w/o arguments/options (osparc integration)
    #
    app = typer.Typer()

    for func in expose:
        app.command(name=func.__name__, help=func.__doc__)(create_service_cli(func))

    return app


if __name__ == "__main__":
    app = create_cli(expose=[salute, hello])
    app()
