import asyncio
from contextlib import AsyncExitStack, asynccontextmanager
from pathlib import Path

from aiofiles.tempfile import TemporaryDirectory


class Entity:
    def __init__(self):
        self._aiostack = AsyncExitStack()

    async def start(self):
        tmpdir = await self._aiostack.enter_async_context(
            TemporaryDirectory(prefix="Entity_")
        )

        self.tmpdir = Path(tmpdir)
        foo = self.tmpdir / "foo"
        foo.touch()

        assert foo.exists()

    async def teardown(self):
        await self._aiostack.aclose()
        assert not self.tmpdir.exists()


@asynccontextmanager
async def entity_context(e: Entity):
    try:
        await e.start()
        yield e
    finally:
        await e.teardown()


async def testit(fail: bool = False):
    async with entity_context(Entity()) as e:
        print(e)
        # raise ValueError()


asyncio.run(testit(True))
