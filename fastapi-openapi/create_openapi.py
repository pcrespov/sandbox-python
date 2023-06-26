import json

from fastapi import FastAPI
from pydantic import AnyUrl, BaseModel, conint


class StuffGet(BaseModel):
    int: conint(gt=33)
    link: AnyUrl  # <<<---- ISSUE with these types


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


@app.get("/stuff", response_model=StuffGet)
async def get_stuff():
    pass


if __name__ == "__main__":
    with open("openapi.json", "wt") as fh:
        json.dump(app.openapi(), fh, indent=1)
