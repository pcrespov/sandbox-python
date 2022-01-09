import inspect
import json

#
# https://docs.aiohttp.org/en/stable/web_advanced.html#aiohttp-web-cleanup-ctx
#
from contextlib import contextmanager, suppress

from aiohttp import web


async def good_context(app: web.Application):
    print("STARTUP good_context")

    app["good_context"] = "state"

    yield

    print("CLEANUP good_context")


async def bad_context(app: web.Application):
    print("STARTUP good_context")

    if app["good_context"]:
        raise ValueError()
    app["bad_context"] = "state"

    yield

    print("CLEANUP bad_context")


def create_msg(when):
    async def dump_state(app: web.Application):
        print(f"{when} app-state:", json.dumps(app._state))

    return dump_state


if __name__ == "__main__":
    app = web.Application()

    # aiohttp guarantees that cleanup code is called if and only if startup code was successfully finished.?????
    app.cleanup_ctx.append(good_context)
    # app.cleanup_ctx.append(bad_context)

    app.on_startup.append(create_msg("STARTUP"))
    app.on_shutdown.append(create_msg("SHUTDOWN"))
    app.on_cleanup.append(create_msg("CLEANUP"))

    web.run_app(app)
