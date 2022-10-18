import os
import subprocess
import sys
from pathlib import Path

current_dir = Path(sys.argv[0] if __name__ == "__main__" else __file__).resolve().parent


def test_make_hi():
    expected_path = current_dir / "hi.txt"

    expected_path.unlink(missing_ok=True)

    subprocess.run(
        ["/bin/bash", "-c", "make hi.txt"],
        cwd=current_dir,
        check=True,
        capture_output=True,
    )

    assert expected_path.exists()


def test_activate():

    p = subprocess.run(
        ["python -m venv virtualenv && virtualenv/bin/activate && which python"],
        cwd=current_dir,
        check=True,
        shell=True,
    )
    assert p.returncode == os.EX_OK
