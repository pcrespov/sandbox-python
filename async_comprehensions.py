# https://peps.python.org/pep-0530/

import asyncio


async def async_iter():
    for n in range(5):
        await asyncio.sleep(0.1)
        yield n


async def trial():
    # l1 = []
    # async for i in async_iter():
    #    l1.append(i)
    # print(l1)

    l2 = [i async for i in async_iter()]
    # print(l2)


def main():
    asyncio.run(trial())


if __name__ == "__main__":
    main()
