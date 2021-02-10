#
# https://docs.aiohttp.org/en/stable/web_advanced.html
# https://docs.python.org/3/library/asyncio-task.html#asyncio.Task.cancel
#
#
#


import asyncio
import io
from asyncio import CancelledError, iscoroutinefunction
from asyncio.coroutines import iscoroutine
from asyncio.tasks import sleep

import aiohttp_debugtoolbar
from aiohttp import web
from aiohttp.web_response import json_response
from aiohttp_debugtoolbar import toolbar_middleware_factory


def log_exc(exception_cls, *, suppress=False):
    def decorator(coro):
        assert iscoroutinefunction(coro)

        async def wrapper(*args, **kwargs):
            try:
                return await coro(*args, **kwargs)
            except exception_cls as err:
                print("Got", type(err), err)
                if not suppress:
                    print("suppressing")
                    raise err

        return wrapper

    return decorator


@log_exc(CancelledError)
async def go(t=3, raise_err=False, symbol="."):
    print(symbol)

    await asyncio.sleep(t)

    if raise_err:
        raise ValueError("BOOM")

    print("DONE")
    return t


def print_report(stream=None):
    print("Tasks in the loop", "-" * 10, file=stream)
    # - done tasks are removed from the loop (not sure when, though ...)
    #
    snapshot = asyncio.all_tasks()
    cancelled, done = 0, 0
    for i, t in enumerate(snapshot):
        cancelled += 1 if t.cancelled() else 0
        done += 1 if t.done() else 0
        print(i, t, file=stream)

    print("cancelled:", cancelled, file=stream)
    print("done     :", done, file=stream)
    print("run      :", len(snapshot) - cancelled - done, file=stream)
    print(file=stream)


# Routes ------------------------------------
routes = web.RouteTableDef()


@routes.get("/")
async def hello(request: web.Request):
    print(".", request)
    return web.Response(text="Hoi zäme")


@routes.get("/fire")
async def fire_n_forget(request: web.Request):

    task = asyncio.create_task(
        go(request.query.get("t", 10), request.query.get("raise", False))
    )
    raise web.HTTPOk()


@routes.get("/multi")
async def multitask(request: web.Request):
    n = int(request.query.get("n", 10))

    # gather seems to shield ??
    results = await asyncio.gather(*[go(t=i + 1) for i in range(n)])
    return web.json_response(data=results)


@routes.get("/info")
async def info(request: web.Request):
    stream = io.StringIO()
    print_report(stream)
    return web.Response(text=stream.getvalue())


# Signals on_startup/on_clenaup/cleanup_ctx -----------


async def on_startup(app: web.Application):
    print("THE START", "-" * 100)
    print("on startup", app)


async def on_cleanup(app: web.Application):
    print("on cleanup", app)
    print_report()
    print("THE END", "-" * 100)


async def run_gc(app: web.Application):
    try:
        n = 0
        while True:
            n += 1
            await asyncio.sleep(1)
            print("gc-ing", n)

    except CancelledError:
        print("oh boy, they don't need me anymore")
        print("A chance to cleanup my stuff  ... ")
        await asyncio.sleep(2)
        print("done")
        raise


async def background_gc(app: web.Application):
    # startup
    print("starting background task with gc")
    gc_task = asyncio.create_task(run_gc(app))

    yield

    # cleanup
    try:
        print("stopping gc")
        # by doing it here, we control
        # the moment in which this happens
        gc_task.cancel()
        await gc_task

    except Exception as err:
        print(type(err), "handled")
        # NOTE: if we do not stop this, it propagates will avoid cleanup
        # raise err
    finally:
        print("background task stopped")


def init() -> web.Application:
    app = web.Application()
    aiohttp_debugtoolbar.setup(app)

    app.add_routes(routes)

    app.on_startup.append(on_startup)
    app.on_cleanup.append(on_cleanup)

    # A background task here is a task that is scheduled upon app init
    # and runs in the brackground (possible indefinitely) of the application
    app.cleanup_ctx.append(background_gc)

    # Cancellations happen later

    return app


print("Debug bar in http://localhost:8080/_debugtoolbar/")
web.run_app(init())

# Contro-C -> sends signal and calls to cleanup
