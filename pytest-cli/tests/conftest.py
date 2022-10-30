from pathlib import Path

import pytest


def pytest_addoption(parser: pytest.Parser):
    parser.addoption("--target-dir", help="Base directory to target test upon")


@pytest.fixture
def target_dir(pytestconfig) -> Path:
    dir_path = pytestconfig.getoption("--target-dir")
    assert dir_path
    dir_path = Path(dir_path)
    assert dir_path.exists()
    return dir_path
