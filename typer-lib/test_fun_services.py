import json
from pathlib import Path

import auto_cli_main
import pytest
from auto_cli_main import app
from pydantic import BaseModel
from pytest import MonkeyPatch
from typer.testing import CliRunner

runner = CliRunner()


class ContainerSpec(BaseModel):
    Command: list


@pytest.fixture
def container_environ(
    monkeypatch: MonkeyPatch, tmp_path: Path, cmd: str, kwargs: dict
) -> ContainerSpec:
    """Emulates environ that the runner finds when container starts"""

    # fake i/o mounts
    input_dir = tmp_path / "inputs"
    input_dir.mkdir(parents=True)

    # dask-sidecar created inputs
    (input_dir / "inputs.json").write_text(json.dumps(kwargs))

    outputs_dir = tmp_path / "outputs"
    outputs_dir.mkdir(parents=True)

    # fake envs
    monkeypatch.setenv("INPUT_FOLDER", f"{input_dir}")
    monkeypatch.setenv("OUTPUT_FOLDER", f"{outputs_dir}")

    yield ContainerSpec(Command=["auto_cli_main", cmd])

    # should have an output
    outputs_path = outputs_dir / "outputs.json"
    assert outputs_path.exists()

    outputs = json.loads(outputs_path.read_text())
    print(outputs)


def test_help():
    result = runner.invoke(app, ["--help"])
    assert result.exit_code == 0

    assert "hello" in result.stdout
    assert "salute" in result.stdout


@pytest.mark.parametrize(
    "cmd,kwargs",
    [
        ("hello", {}),
        ("salute", {"name": "pedro", "lastname": "crespo", "formal": False}),
        ("salute", {"name": "pedro", "lastname": "crespo", "formal": True}),
    ],
)
def test_run_services(container_environ: ContainerSpec):

    program_name, command = container_environ.Command
    assert auto_cli_main.__name__ == program_name

    result = runner.invoke(
        app,
        [
            command,
        ],
    )
    assert result.exit_code == 0
    assert "hello" in result.stdout.lower()
