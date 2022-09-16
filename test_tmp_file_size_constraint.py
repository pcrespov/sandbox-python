from typing import Any, Iterator
import pytest
from _pytest.fixtures import FixtureRequest
from _pytest.tmpdir import TempPathFactory
from pydantic import ByteSize, parse_obj_as
from pathlib import Path


MAX_SIZE = parse_obj_as(ByteSize, "3MiB")


@pytest.fixture(scope="function", autouse=True)
def tempdir_size_constraint(
    request: FixtureRequest, tmp_path_factory: TempPathFactory
) -> Iterator[None]:

    assert issubclass(ByteSize, int)

    def _get_folder_size(folder: Path) -> ByteSize:
        return parse_obj_as(
            ByteSize, sum(f.stat().st_size for f in folder.rglob("*") if f.is_file())
        )

    temp_root_dir = tmp_path_factory.getbasetemp().parents[0]  # typically /tmp

    before = _get_folder_size(temp_root_dir)

    yield

    after = _get_folder_size(temp_root_dir)
    diff = parse_obj_as(ByteSize, after - before)

    print(
        f"Size of '{temp_root_dir}'",
        f"{before.human_readable()=}",
        f"{after.human_readable()=}",
        f"{diff.human_readable()=}",
        f"{request.node.nodeid=}",
    )

    assert (
        diff < MAX_SIZE
    ), f"{diff.human_readable()} bigger than limit {MAX_SIZE.human_readable()}"


def test_it(tmp_path: Path):

    with (tmp_path / "fat-file").open("w") as f:
        f.truncate(MAX_SIZE * 2)
