
from datetime import datetime
from typing import Optional

import pytest
from pydantic import BaseModel, ValidationError, validator
from pydantic.dataclasses import dataclass


def test_always():
    # SEE https://pydantic-docs.helpmanual.io/usage/validators/

    class DemoModel(BaseModel):
        ts: Optional[datetime] = None

        # by default validators are not called for fields when a value is not supplied.
        # this can be override with always=True
        # You'll often want to use this together with pre, since otherwise with always=True pydantic would try to validate the default None which would cause an error.
        @validator("ts", pre=True, always=True)
        def set_ts_now(cls, v):
            return v or datetime.now()

    #
    d = DemoModel()

    print(d)
    # > ts=datetime.datetime(2021, 12, 31, 15, 4, 57, 629206)

    assert d.ts is not None

    d = DemoModel(ts="2017-11-08T14:00")
    print(d)
    # > ts=datetime.datetime(2017, 11, 8, 14, 0)

    assert d.ts is not None

    d.ts = "foo"
    assert (
        d.ts == "foo"
    )  # even if it is wrong because by default it does not validate on assignment


def test_validate_assignments():
    # SEE https://pydantic-docs.helpmanual.io/usage/model_config/

    class User(BaseModel):
        class Config:
            max_anystr_length = 10
            validate_assignment = True  # whether to perform validation on assignment to attributes (default: False)
            error_msg_templates = {
                "value_error.any_str.max_length": "max_length:{limit_value}",
            }

        id: int
        name: str = "John Doe"
        signup_ts: datetime = None


    user = User(id="42", signup_ts="2032-06-21T12:00")

    with pytest.raises(ValidationError) as err_info:
        user.name = "x" * 20

    assert isinstance(err_info.value, ValidationError)
    assert len(err_info.value.errors()) == 1

    error = err_info.value.errors()[0]
    print(error)
    assert error["loc"] == ("name",)
    assert error["type"] == "value_error.any_str.max_length" # see 'code' and 'msg_template' in pydantic.errors:AnyStrMinLengthError
    assert error["msg"] == "max_length:10"
    assert "ctx" in error, "thisone is optional but will be included because the error is defined"
    assert error["ctx"] == {"limit_value": 10}

    """
    1 validation error for User
    name
    max_length:10 (type=value_error.any_str.max_length; limit_value=10)
    """
