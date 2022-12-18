from typing import Optional

from aiohttp import web
from pydantic import BaseModel


# Use pydantic BaseModel to validate request body
class ArticleModel(BaseModel):
    name: str
    nb_page: Optional[int]


app = web.Application()


def test_it():
    ...
