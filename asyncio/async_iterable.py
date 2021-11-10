# SEE https://www.python.org/dev/peps/pep-0525/#aiter-and-anext-builtins

import asyncio


async def g1():
    yield 1
    yield 2


async def g2():
    async for v in g1():
        yield v


## emulates the structure of https://github.com/aio-libs/aiodocker/blob/master/aiodocker/services.py#L185
async def fun(n):
    for x in range(n):
        await asyncio.sleep(0.1)
        yield x


def get_iter_coro():
    return fun(4)


async def demo():

    iter_coro = get_iter_coro()
    print(iter_coro)

    async for i in iter_coro:
        print(i)

    print("DONE")
    # for s in await iter_coro:
    #     print(x)

    # async for x in get_iter_coro():
    #     print(x)


asyncio.run(demo())
