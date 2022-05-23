
import json

from fastapi import FastAPI
from pydantic import AnyUrl, BaseModel, conint


class StuffGet(BaseModel):
    int: conint(gt=33)
    #link: AnyUrl


app = FastAPI()


@app.get("/stuff", response_model=StuffGet)
async def get_stuff():
    pass


if __name__ == "__main__":
    with open("openapi.json", "wt") as fh:
        json.dump(app.openapi(), fh, indent=1)
