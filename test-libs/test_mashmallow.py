#pip install -U marshmallow --pre
#pip install -U attr

# See design of https://github.com/marshmallow-code/apispec
# See design of https://github.com/mozillazg/aiobearychat

from marshmallow import Schema, fields, post_load
import attr
from typing import Dict
from pprint import pprint

#https://marshmallow.readthedocs.io/en/3.0/quickstart.html

import datetime as dt

@attr.s(auto_attribs=True)
class User:
    name: str 
    email: str
    created_at: dt.datetime = attr.Factory(dt.datetime.now)

class UserSchema(Schema):
    name = fields.Str(required=True)
    email = fields.Email()
    created_at = fields.DateTime()

    @post_load
    def make_user(self, data: Dict) -> User:
        return User(**data, ggg)


def test_serialize():
    user = User(name="foo", email="foo@bar.com")

    # dump to dict
    schema = UserSchema()
    result = schema.dump(user)
    assert isinstance(result, dict)
    assert user.email == result['email']
    assert user.name == result['name']
    #assert user.created_at == result['created_at']

    # ... to json-like
    json_res = schema.dumps(user)
    assert isinstance(json_res, str)

    # filter
    fschema = UserSchema(only=['name',])
    fresult = fschema.dump(user)
    #assert fresult.keys() == ['name']  # AssertionError: assert dict_keys(['name']) == ['name']

    # deserialize
    result = schema.loads(json_res)
    assert isinstance(result, User)
    pprint(json_res)
    pprint(result)

