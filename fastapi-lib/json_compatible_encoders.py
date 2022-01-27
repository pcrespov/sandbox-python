# 
# https://github.com/samuelcolvin/pydantic/issues/951#issuecomment-552463606
# 
# https://fastapi.tiangolo.com/tutorial/encoder/
# 

#
# Support for pydantic model's dict
# Ensures items in resulting dict are "json friendly"
#
#

from uuid import UUID, uuid4

from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel


class MyModel(BaseModel):
    uid: UUID



a = MyModel(uid=uuid4())


print(a.dict())
print(jsonable_encoder(a))
