from typing import Annotated

from fastapi import Depends, FastAPI
from pydantic import AnyUrl, BaseModel, Field, conint


class BodyModel(BaseModel):
    """Describes Model"""

    foo: int


class StuffGet(BaseModel):
    """Describes response"""

    number: conint(gt=33)
    link: AnyUrl  # <<<---- ISSUE with these types


class ParamsModel(BaseModel):
    param: int = Field(description="describes param", le=3)
    query: int = Field(description="describes query", ge=2)


#
#
# python -c "import auto_models"
# Traceback (most recent call last):
#   File "<string>", line 1, in <module>
#   File "/home/crespo/devp/sandbox-python/datamodel-codegen-lib/auto_models.py", line 10, in <module>
#     class StuffGet(BaseModel):
#   File "pydantic/main.py", line 205, in pydantic.main.ModelMetaclass.__new__
#   File "pydantic/fields.py", line 489, in pydantic.fields.ModelField.infer
#   File "pydantic/schema.py", line 1022, in pydantic.schema.get_annotation_from_field_info
# ValueError: On field "link" the following field constraints are set but not enforced: max_length, min_length.
# For more details see https://pydantic-docs.helpmanual.io/usage/schema/#unenforced-field-constraints

app = FastAPI()


@app.post("/stuff/{param}", response_model=StuffGet)
async def get_stuff(body: BodyModel, params: Annotated[ParamsModel, Depends()]):
    pass
