from datetime import datetime, timedelta

from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel


class TimeModel(BaseModel):
    delta: timedelta
    dt: datetime


tm = TimeModel(delta="M", dt=datetime.now())
print(tm)
print(jsonable_encoder(tm))
