from dataclasses import dataclass

import aiohttp
from aiohttp import web


@dataclass
class A:
    x: int


async def hi(request):
    print(app[A.__name__])
    return web.Response(text="hoi zaeme")


app = web.Application()
app.add_routes([web.get("/", hi)])



# using the class itself 
# app[A] = A(x=3)
# or
app[A.__name__] = A(x=3)


if __name__ == "__main__":
    web.run_app(app)
