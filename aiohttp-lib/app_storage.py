from dataclasses import dataclass

import aiohttp
from aiohttp import web


@dataclass
class A:
    x: int


# ROUTES
async def hi(request):
    print(request.app[A.__name__])
    return web.Response(text="hoi zaeme")


# EVENTS
async def on_startup(app: web.Application):
    # using the class itself
    # app[A] = A(x=3)
    # or
    app[A.__name__] = A(x=3)


async def on_cleanup(app: web.Application):
    # NOTE: DeprecationWarning: Changing state of started or joined application is deprecated
    # del app[A.__name__]
    # app[A.__name__] = None
    print("app state", dict(app))


# MAIN
def create_app():
    app = web.Application()
    app.add_routes([web.get("/", hi)])
    app.on_startup.append(on_startup)
    app.on_cleanup.append(on_cleanup)
    return app


if __name__ == "__main__":
    web.run_app(create_app())
