from aiohttp import web
from aiohttp.web import Application, Request, RouteDefTable

routes = RouteDefTable()


@routes.get("/health")
async def health(request: Request):
    pass


app = Application(__name__)
app.router.add(routes)
web.run(app, host="0.0.0.0")