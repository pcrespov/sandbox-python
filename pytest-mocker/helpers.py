import asyncio

async def coro(n=1):
    await asyncio.sleep(n)
    return 3
