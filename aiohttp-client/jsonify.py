import asyncio
import json
from datetime import datetime
from typing import Any, Callable, Optional
from uuid import UUID, uuid4

import orjson
import ujson
from aiohttp import ClientSession


class _UuidEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, UUID):
            # NOTE: careful here!
            return str(o)
        return json.JSONEncoder.default(self, o)


def json_dumps(obj: Any, **kwargs):
    """json.dumps with UUID encoder"""
    return json.dumps(obj, cls=_UuidEncoder, **kwargs)


def orjson_dumps(
    v, *, default: Optional[Callable[[Any], Any]] = None, indent: Optional[int] = None
) -> str:
    # SEE https://github.com/ijl/orjson
    # - orjson.dumps returns *bytes*, to match standard json.dumps we need to decode

    # Cannot use anymore human readable prints like ``print(model.json(indent=2))``
    # because it does not include indent option. This is very convenient for debugging
    # so if added, it switches to json
    if indent:
        return json.dumps(v, default=default, indent=indent)

    return orjson.dumps(v, default=default).decode()


def json_dumps_hybrid(obj: Any, **common_kwags):
    try:
        # Fast does not support custom encoders
        # SEE https://github.com/ultrajson/ultrajson/issues/124
        return ujson.dumps(obj, **common_kwags)
    except TypeError:
        return json_dumps(obj, **common_kwags)





async def main():

    for jsonify in (json_dumps, orjson_dumps, ujson.dumps, json_dumps_hybrid):
        print(jsonify.__name__, "*" * 100)
        try:
            tic = datetime.now()

            async with ClientSession(json_serialize=jsonify) as session:

                async with session.get(
                    "http://httpbin.org/anything", json={"uuid": uuid4()}
                ) as resp:
                    print(resp.status)
                    print(await resp.text())

            print("ELAPSED", datetime.now() - tic, "secs")

        except TypeError as err:
            print("Failed", err)


if __name__ == "__main__":
    asyncio.run(main())
