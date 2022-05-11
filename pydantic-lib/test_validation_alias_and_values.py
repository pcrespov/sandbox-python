from pydantic import BaseModel, Field, validator


class A(BaseModel):
    a: int = Field(..., ge=0, alias="aliasA")
    b: int = Field(..., ge=0)
    c: int = Field(..., alias="aliasC", ge=33)


    # https://pydantic-docs.helpmanual.io/usage/validators/#pre-and-per-item-validators

    @validator("c", pre=True)
    def check_other_pre(cls, v, values):
        # since pre=True, the value here is before annotation is validated
        assert "a" in values  # even if it has an alias
        assert "b" in values
        return v + 33
        # modifies
        # what returns, the annotation constraints are validated then

    @validator("c")
    def check_other_post(cls, v, values):
        # annotation constraints already validated
        assert v >= 33

        # everything is in values
        assert "a" in values
        assert "b" in values
        return v




class B(A):
    d: int = 0


    @validator("d", always=True)
    def check_d(cls, v, values):
        # values contain *validated* fields ... but if they fail, they are not passed!!
        
        assert "a" in values # if "a" is invalid, then is not included in values!!
        assert "b" in values
        assert "c" in values
        return v

    class Config:
        validate_assignment = True





def test_it():
    # construct with alias but refered inside with field-names
    z = A(aliasA=1, b=3, aliasC=2)

    assert z.a == 1
    assert z.b == 3
    assert z.c == 2 + 33


def test_b():
    z = B(aliasA=1, b=3, aliasC=44)

    assert z.d == 0

    z.d = 33
    assert z.d == 33



