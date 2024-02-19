import socketio
from aiohttp import web


def create_app():
    # SEE https://python-socketio.readthedocs.io/en/latest/server.html#aiohttp
    sio = socketio.AsyncServer(
        async_mode="aiohttp",
        cors_allowed_origins=[
            "http://localhost:5000",
            "https://admin.socket.io",
        ],
    )
    sio.instrument(
        auth={
            "username": "admin",
            "password": "adminadmin",
        }
    )

    app = web.Application()

    @app.get("/home")
    async def home(request: web.Request):
        assert request
        return web.Response(text="Home")

    sio.attach(app)
    return app


if __name__ == "__main__":
    web.run_app(create_app())
