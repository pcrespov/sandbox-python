from fastapi import FastAPI
from fastapi.testclient import TestClient
import asyncio


app = FastAPI()


@app.get("/error")
async def _fail():
    await asyncio.wait_for(asyncio.sleep(100), timeout=1)


def test_it():
    with TestClient(app) as client:
        r = client.get("/error")
        print("response", r)
