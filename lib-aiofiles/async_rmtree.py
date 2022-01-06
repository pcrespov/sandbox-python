import shutil
import asyncio

from pathlib import Path


from aiofiles.os import remove
from aiofiles.os import wrap as sync_to_async


# https://docs.python.org/3/library/os.html#os.remove
# https://docs.python.org/3/library/shutil.html#shutil.rmtree

_rmtree = sync_to_async(shutil.rmtree)


async def rm(path: Path, onerror=None, **kwargs):
    # kwargs => loop=None, executor=None, **syncfun_kwargs
    try:
        await remove(path, **kwargs)
    except IsADirectoryError:
        await _rmtree(path, onerror=onerror, **kwargs)


async def rmtree(dirpath: Path, keep_folder=False, onerror=None, **kwargs):
    if keep_folder:
        await asyncio.gather(
            *[rm(child, on_error=None, **kwargs) for child in dirpath.glob("*")]
        )
    else:
        await _rmtree(dirpath, onerror=onerror, **kwargs)
