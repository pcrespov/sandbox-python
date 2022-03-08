# from https://github.com/Maillol/aiohttp-pydantic#example

from typing import Optional

from aiohttp import web
from aiohttp_pydantic import PydanticView
from pydantic import BaseModel


# Use pydantic BaseModel to validate request body
class ArticleModel(BaseModel):
    name: str
    nb_page: Optional[int]


# Create your PydanticView and add annotations.
class ArticleView(PydanticView):

    async def post(self, article: ArticleModel):
        return web.json_response({'name': article.name,
                                  'number_of_page': article.nb_page})

    async def get(self, with_comments: bool=False):
        return web.json_response({'with_comments': with_comments})


app = web.Application()
app.router.add_view('/article', ArticleView)
web.run_app(app)
