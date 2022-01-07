import glob
from pathlib import Path
import os
import re
from fnmatch import fnmatch
from typing import Optional, List


gitignore = re.findall(r"^[^#\s]+", Path(".gitignore").read_text(), re.MULTILINE)
#
#
# exclude patterns would not work as in https://git-scm.com/docs/gitignore#_pattern_format
#    /foo/*
#    !/foo/bar

exclude = [
    ".venv/*",
    ".git/*",
    "*.pyc",
    "*.so",
    "pydantic-lib/create_new_model_by_excluding_fields_From_base.py",
    "*.py",
]


def iter_files(basedir: Path, exclude: Optional[List] = None):
    exclude = exclude or []
    for f in basedir.rglob("*"):
        if f.is_file() and not any(fnmatch(f, p) for p in exclude):
            yield f
