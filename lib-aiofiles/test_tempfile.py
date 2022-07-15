import asyncio
import tempfile
from contextlib import asynccontextmanager, contextmanager
from pathlib import Path
from typing import AsyncIterator

import aiofiles
import aiofiles.os
import aiofiles.tempfile
import pytest

CONTENT = "stuff" * 10_000


def sample(n):
    with tempfile.TemporaryDirectory(prefix=f"sample_{n}") as tmpdir:
        fpath = Path(tmpdir) / "docker-compose.yml"
        # assert fpath.parent.exists()

        with open(fpath, "w") as fh:
            fh.write(CONTENT)

        # assert fpath.exists()

    # assert not fpath.exists()
    return fpath


#
# aio_sample
#
async def aio_sample(n):
    async with aiofiles.tempfile.TemporaryDirectory(prefix=f"sample_{n}") as tmpdir:
        fpath = Path(tmpdir) / "docker-compose.yml"
        # assert fpath.parent.exists()

        async with aiofiles.open(fpath, "w") as fh:
            await fh.write(CONTENT)

        # assert fpath.exists()

    # assert not fpath.exists()
    return fpath


#
# aio_sample2
#
@asynccontextmanager
async def aio_write_tmp_file(file_contents: str) -> AsyncIterator[Path]:
    """Disposes of file on exit"""
    # pylint: disable=protected-access,stop-iteration-return
    file_path = Path("/") / f"tmp/{next(tempfile._get_candidate_names())}"  # type: ignore
    async with aiofiles.open(file_path, mode="w") as tmp_file:
        await tmp_file.write(file_contents)
    try:
        yield file_path
    finally:
        await aiofiles.os.remove(file_path)


async def aio_sample2(n):
    async with aio_write_tmp_file(CONTENT) as fpath:
        await asyncio.sleep(0.1)
        # assert fpath.exists()

    # assert not fpath.exists()
    return fpath


Ns = (10, 100, 1_000, 10_000)


@pytest.mark.parametrize("N", Ns)
async def test_aiofiles(N):
    results = await asyncio.gather(
        *(aio_sample(n) for n in range(N)), return_exceptions=True
    )
    # assert not any(isinstance(r, Exception) for r in results)
    # assert len(set(results)) == N


@pytest.mark.parametrize("N", Ns)
async def test_aiofiles2(N):
    results = await asyncio.gather(
        *(aio_sample2(n) for n in range(N)), return_exceptions=True
    )
    # assert not any(isinstance(r, Exception) for r in results)
    # assert len(set(results)) == N


@pytest.mark.parametrize("N", Ns)
async def test_sync_files(N):
    results = [sample(n) for n in range(N)]
    # assert len(set(results)) == N


# pytest --durations=0 --asyncio-mode=auto test_tempfile.py
#
#
# 9.54s call     test_tempfile.py::test_aiofiles[10000]
# 6.42s call     test_tempfile.py::test_sync_files[10000]
# 0.85s call     test_tempfile.py::test_aiofiles[1000]
# 0.62s call     test_tempfile.py::test_sync_files[1000]
# 0.09s call     test_tempfile.py::test_aiofiles[100]
# 0.07s call     test_tempfile.py::test_sync_files[100]
# 0.01s call     test_tempfile.py::test_sync_files[10]
# 0.01s call     test_tempfile.py::test_aiofiles[10]
# 0.01s call     test_tempfile.py::test_sync_files[1]
# 0.01s call     test_tempfile.py::test_aiofiles[1]


# 9.60s call     test_tempfile.py::test_aiofiles[10000]
# 7.64s call     test_tempfile.py::test_aiofiles2[10000]
# 7.31s call     test_tempfile.py::test_sync_files[10000]
# 1.09s call     test_tempfile.py::test_aiofiles[1000]
# 0.63s call     test_tempfile.py::test_sync_files[1000]
# 0.61s call     test_tempfile.py::test_aiofiles2[1000]
# 0.16s call     test_tempfile.py::test_aiofiles2[100]
# 0.15s call     test_tempfile.py::test_aiofiles[100]
# 0.12s call     test_tempfile.py::test_aiofiles2[10]
# 0.07s call     test_tempfile.py::test_sync_files[100]
# 0.02s call     test_tempfile.py::test_aiofiles[10]
# 0.02s call     test_tempfile.py::test_sync_files[10]


# commenting asserts
# 8.01s call     test_tempfile.py::test_aiofiles[10000]
# 6.16s call     test_tempfile.py::test_aiofiles2[10000]
# 6.03s call     test_tempfile.py::test_sync_files[10000]
# 0.90s call     test_tempfile.py::test_aiofiles[1000]
# 0.58s call     test_tempfile.py::test_sync_files[1000]
# 0.54s call     test_tempfile.py::test_aiofiles2[1000]
# 0.16s call     test_tempfile.py::test_aiofiles2[100]
# 0.12s call     test_tempfile.py::test_aiofiles2[10]
# 0.11s call     test_tempfile.py::test_aiofiles[100]
# 0.08s call     test_tempfile.py::test_sync_files[100]
# 0.02s call     test_tempfile.py::test_aiofiles[10]
# 0.01s call     test_tempfile.py::test_sync_files[10]
# 0.01s setup    test_tempfile.py::test_sync_files[10]
