from fastapi import FastAPI
from fastapi.responses import JSONResponse, RedirectResponse
from pydantic import BaseModel

app = FastAPI()


@app.get("/typer")
async def redirect_typer():
    return RedirectResponse("https://typer.tiangolo.com")


@app.get("/fastapi", response_class=RedirectResponse)
async def redirect_fastapi():
    return "https://fastapi.tiangolo.com"


class MyModel(BaseModel):
    x: int


@app.get("/mymodel", response_model=MyModel)  # OAS
async def my_model():
    return {"x": 42}  # validates


@app.get("/mymodel_2", response_model=MyModel)  # OAS
async def my_model_2():
    return JSONResponse({"x": 42})  # how does it reacts to this?


@app.get("/mymodel_invalid", response_model=MyModel)
async def my_model_invalid():
    return JSONResponse({"zzz": 42})  # validates?


@app.get("/other_model", response_class=JSONResponse)
async def other_model():
    return {"zzz": 42}


@app.get("/hybrid", response_model=MyModel)
async def hybrid(flag: bool = True):
    if flag:
        return MyModel(x=43)
    return RedirectResponse("/mymodel")
