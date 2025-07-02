# /// script
# requires-python = ">=3.11"
# dependencies = [
#     "aiohptt",
#     "pytest",
#     "pytest-ascynio",
# ]
# ///

# SEE https://docs.aiohttp.org/en/stable/testing.html
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