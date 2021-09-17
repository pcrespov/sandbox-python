#
# - https://docs.python.org/3/library/asyncio-task.html#timeouts
#
import asyncio


async def eternity():
    await asyncio.sleep(36000)
    print("yay!")


async def main():
    try:
        await asyncio.wait_for(eternity(), timeout=1.0)

    except asyncio.TimeoutError:
        print("asyncio timeout!")
    except TimeoutError:
        # WARNING: NOT the same https://docs.python.org/3/library/exceptions.html#TimeoutError
        print("built-in timeout")



if __name__ == "__main__":
    asyncio.run(main())