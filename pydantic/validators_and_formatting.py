from pydantic import BaseModel, constr, validator

sample = "A high-level language, primarily intended for numerical computations. It provides a convenient comma"
MAX = 10 # len(sample)+1


class User(BaseModel):
    name: str = "John Doe"
    short_description: constr(min_length=2, max_length=MAX+1)

    @validator("short_description", pre=True)
    @classmethod
    def truncate_to_short(cls, v):
        if len(v)>MAX:
            return v[:MAX] + "…"
        return v 

print( User(short_description="0123456789") )
print( User(short_description="0123456789*") )


