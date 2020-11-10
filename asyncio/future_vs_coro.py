#
# This answer does NOT seem to work as described!
#
# https://stackoverflow.com/questions/37278647/fire-and-forget-python-async-await/37345564#37345564
#
#
import asyncio


async def async_foo():
    print("async_foo started")
    await asyncio.sleep(1)
    print("async_foo done")


async def go_forever():
    n = 0
    while True:
        print(f"t={n}")
        await asyncio.sleep(1)  # this is stopped here after the loop is done!
        n += 1


async def main():
    # NOTE: how go_forever is finished with coro is done
    asyncio.ensure_future(go_forever())
    await asyncio.sleep(10)


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
