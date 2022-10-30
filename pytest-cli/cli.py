import sys
from pathlib import Path

import pytest

CURRENT_DIR = Path(sys.argv[0] if __name__ == "__main__" else __file__).resolve().parent


class MyPlugin:
    def pytest_sessionfinish(self):
        print("*** test run reporting finishing")


if __name__ == "__main__":
    extra_args = []
    if len(sys.argv) > 1:
        extra_args = sys.argv[1:]

    sys.exit(
        pytest.main(
            ["-vv", f"{CURRENT_DIR /'tests'}"] + extra_args, plugins=[MyPlugin()]
        )
    )
