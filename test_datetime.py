from datetime import timedelta

from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel


class TimeModel(BaseModel):
    delta: timedelta


models = [TimeModel(delta=60), TimeModel(delta="01:00"), TimeModel(delta="01:00")]
for m in models:
    print(m, jsonable_encoder(m))
