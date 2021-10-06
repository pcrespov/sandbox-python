import asyncio
import httpx
from time import time


client = httpx.AsynClient()


async def measure(url, n=100):
    tic = time()
    coros = [ client.get(url) for _ in range(n) ]
    results = await asyncio.gather(**coros)
    toc = time()
    print(url, f"{n} simultaneous requests", "total time:", toc-tic)



async def blocking_async():
    a = asyncio.run_task(measure('http://127.0.0.1:8000/fib/35'), n=1)
    b = asyncio.run_task(measure('http://127.0.0.1:8000/fast'), n=1)
    print(await b)
    print(await a)


