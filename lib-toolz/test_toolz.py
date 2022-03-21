# https://github.com/pytoolz/toolz
# https://toolz.readthedocs.io/en/latest/control.html

import json
from pathlib import Path

import httpx
import pytest
from toolz import concat, frequencies, map


@pytest.fixture(scope="session")
def book_path(tmp_path: Path) -> Path:
    dst = tmp_path / "tale-of-two-cities.txt"
    r = httpx.get("http://www.gutenberg.org/cache/epub/98/pg98.txt")
    dst.write_text(r.text)
    print(dst.stat())

    return dst


def test_lazy():
    with httpx.stream("GET", "http://www.gutenberg.org/cache/epub/98/pg98.txt", follow_redirects=True) as r:
        book = r.iter_lines()
        loud_book = map(str.upper, book)

        f = frequencies(concat(loud_book))
        print(json.dumps(f, indent=2, sort_keys=True))
