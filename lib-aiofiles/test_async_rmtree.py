from async_rmtree import rmtree
import pytest
import concurrent.futures
import os
from pathlib import Path
from stat import S_IREAD, S_IWRITE

pytestmark = pytest.mark.asyncio


def remove_readonly(func, path, exc_info):
    print(func, path, exc_info)
    os.chmod(path, S_IWRITE)
    os.unlink(path)


@pytest.fixture
def fake_folder(tmp_path: Path):
    folder = tmp_path / "root"

    # create folder
    folder.mkdir()
    (folder / "a_file").touch()
    (folder / "a_dir").mkdir()
    (folder / "a_link").symlink_to(folder / "a_file", False)
    (folder / "a_dir_link").symlink_to(folder / "a_dir", True)
    (folder / "a_read_only_file").touch(S_IREAD)

    os.system(f"ls -la {folder}")
    # TODO: add a file w/o write access

    yield folder

    if folder.exists():
        os.system(f"ls -la {folder}")


async def test_1(fake_folder: Path):

    assert fake_folder.exists()
    assert any(fake_folder.rglob("*"))

    await rmtree(fake_folder, keep_folder=True)

    assert fake_folder.exists()
    assert not any(fake_folder.rglob("*"))


async def test_2(fake_folder: Path):

    assert fake_folder.exists()
    assert any(fake_folder.rglob("*"))

    await rmtree(fake_folder, keep_folder=False, on_error=remove_readonly)

    assert not fake_folder.exists()


async def test_3(fake_folder: Path):

    assert fake_folder.exists()
    assert any(fake_folder.rglob("*"))

    with concurrent.futures.ProcessPoolExecutor() as pool:
        await rmtree(fake_folder, keep_folder=True, executor=pool)

    assert fake_folder.exists()
    assert not any(fake_folder.rglob("*"))


async def test_4(fake_folder: Path):

    assert fake_folder.exists()
    assert any(fake_folder.rglob("*"))

    with concurrent.futures.ThreadPoolExecutor() as pool:
        await rmtree(fake_folder, keep_folder=True, executor=pool)

    assert fake_folder.exists()
    assert not any(fake_folder.rglob("*"))
