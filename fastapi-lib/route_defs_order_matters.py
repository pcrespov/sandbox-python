# https://fastapi.tiangolo.com/tutorial/path-params/#order-matters
#

from fastapi import FastAPI

app = FastAPI()


@app.get("/users/me")
async def read_user_me():
    return {"user_id": "the current user"}


@app.get("/users/{user_id}")
async def read_user(user_id: str):
    return {"user_id": user_id}


@app.get("/users")
async def list_users():
    return [ {"user_id": user_id} for user_id in range(4) ]