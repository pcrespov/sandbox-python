import pytest

from aiohttp import web

async def previous(request):
    if request.method == 'POST':
        request.app['value'] = (await request.post())['value']
        return web.Response(body=b'thanks for the data')
    return web.Response(
        body='value: {}'.format(request.app['value']).encode('utf-8'))


@pytest.fixture
def cli(loop, aiohttp_client):
    app = web.Application()
    app.router.add_get("/", previous)
    app.router.add_post("/", previous)

    client = loop.run_until_complete(aiohttp_client(app))
    return client
    

async def test_set_value(cli):
    resp = await cli.post("/", data={'value': 'foo'})
    assert resp.status == 200