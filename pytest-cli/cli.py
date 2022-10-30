import sys
from pathlib import Path

import pytest

CURRENT_DIR = Path(sys.argv[0] if __name__ == "__main__" else __file__).resolve().parent


class MyPlugin:
    def pytest_sessionfinish(self):
        print("*** test run reporting finishing")


if __name__ == "__main__":
    print(f"{CURRENT_DIR=}")
    print("Running", sys.argv, "...")
    # Somehow if the __pycache__ external gets copied in the container, then it cannot see the

    extra_args = []
    if len(sys.argv) > 1:
        extra_args = sys.argv[1:]

    print(["-vv", f"{CURRENT_DIR /'tests'}"] + extra_args)
    sys.exit(
        pytest.main(
            [
                "-vv",
                "--log-level=DEBUG",
                "--cache-clear",
                "--override-ini=cache_dir=/tmp/.pytest_cache",
                f"{CURRENT_DIR /'tests'}",
            ]
            + extra_args,
            plugins=[MyPlugin()],
        )
    )
