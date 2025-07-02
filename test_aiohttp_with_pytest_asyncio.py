# /// script
# requires-python = ">=3.11"
# dependencies = [
#     "aiohptt",
#     "pytest",
#     "pytest-ascynio",
# ]
# ///

# pylint: disable=redefined-outer-name
# pylint: disable=too-many-arguments
# pylint: disable=too-many-positional-arguments
# pylint: disable=too-many-statements
# pylint: disable=unused-argument
# pylint: disable=unused-variable

# SEE https://docs.aiohttp.org/en/stable/testing.html
# SEE https://pytest-asyncio.readthedocs.io/en/stable/

from aiohttp import web


pytest_plugins = [
    'aiohttp.pytest_plugin', # No need to install pytest-aiohttp separately
    ]

async def hello(request):
    return web.Response(text='Hello, world')


async def test_hello(aiohttp_client):
    app = web.Application()
    app.router.add_get('/', hello)
    client = await aiohttp_client(app)
    resp = await client.get('/')
    assert resp.status == 200
    text = await resp.text()
    assert 'Hello, world' in text
