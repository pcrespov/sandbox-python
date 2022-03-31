from importlib.resources import path
import sys
from pathlib import Path

CURRENT_DIR = Path( sys.argv[0] if __name__ == "__main__" else __file__).resolve().parent
sys.path.insert(0, str(CURRENT_DIR / ".." / "src") )

def test_foo():
    assert 1+1
