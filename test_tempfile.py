import tempfile
from pathlib import Path


def touch_tmpfile(extension=".dat") -> Path:
    with tempfile.NamedTemporaryFile(delete=False, suffix=extension) as file_handler:
        return Path(file_handler.name)

path = touch_tmpfile()
assert path.exists()
print(path)

