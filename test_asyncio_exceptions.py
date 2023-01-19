import asyncio


async def iter_1():
    for value in range(3):
        asyncio.sleep(0.1)
        if value == 2:
            raise ValueError
        yield value


async def iter_0():
    async for value in iter_1():
        yield value


async def demo():
    async for value in iter_0():
        print(value)


if __name__ == "__main__":
    asyncio.run(demo())
