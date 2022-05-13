from typing import Optional

from fastapi import FastAPI
from pydantic import BaseModel, Field, NonNegativeInt, PositiveInt

app = FastAPI()

## https://sqlmodel.tiangolo.com/tutorial/fastapi/multiple-models/



class HeroBase(BaseModel):
    name: str = Field()
    secret_name: str
    age: Optional[PositiveInt] = Field(default=None)


class Hero(HeroBase):
    # r/w
    id: Optional[int] = Field(default=None)



class HeroGet(HeroBase):
    id: NonNegativeInt



class HeroCreate(BaseModel):
    pass



DATA = {}

@app.post("/heroes/", response_model=HeroGet)
def create_hero(hero: HeroCreate):
    
    h = Hero.from_orm(hero)
    DATA[0] = h 
    h.id = 0
    return h

