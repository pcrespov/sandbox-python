from typing import List

import pytest
from pydantic import BaseModel, ValidationError, conint


class Location(BaseModel):
    lat = 0.1
    lng = 10.1

class Model(BaseModel):
    is_required: float
    gt_int: conint(gt=42) # constraint annotations
    list_of_ints: List[int] = None
    a_float: float = None
    recursive_model: Location = None




def test_annotation_validation():
    bad_data = dict(
        list_of_ints=["1", 2, "bad"],
        a_float="not a float",
        recursive_model={"lat": 4.2, "lng": "New York"},
        gt_int=21,
    )

    with pytest.raises(ValidationError) as err_info:
        Model(**bad_data)

    e = err_info.value
    assert isinstance(e, ValidationError)
    # 0:{'loc': ('is_required',), 'msg': 'field required', 'type': 'value_error.missing'}
    # 1:{'loc': ('gt_int',), 'msg': 'ensure this value is...er than 42', 'type': 'value_error.number.not_gt', 'ctx': {'limit_value': 42}}
    # 2:{'loc': ('list_of_ints', 2), 'msg': 'value is not a valid integer', 'type': 'type_error.integer'}
    # 3:{'loc': ('a_float',), 'msg': 'value is not a valid float', 'type': 'type_error.float'}
    # 4:{'loc': ('recursive_model', 'lng'), 'msg': 'value is not a valid float', 'type': 'type_error.float'}
    print(e)
    print(e.errors())
    print(e.json())
