from pydantic import BaseModel, create_model

class M1(BaseModel):
    value: str



# How to ADD fields to a common base?
# Say  M2 *extends* M1 


# option a: inheritance
#
# PROS: 
#   - simple
#   - can be used also to override base
# CONS:
#   - coupled to changes of M1
#   
class M2a(M1):
    version: str

print("M2a:", M2a.schema_json(indent=2))

# option b: double inheritance (kind of a mixin)
#
#  PROS: 
#    - can reuse same extension for other models
#  CONS:
#    - verbose
class Ext(BaseModel):
    version: str

class M2b(M1, Ext):
    pass

print("M2b:", M2b.schema_json(indent=2))


# option c: dynamic creator
#
# TOO COMPLEX
M2a.__fields__.union(Ext.__fields__)

M2c = creat_model("M2c", )
print("M2c:", M2c.schema_json(indent=2))

#
#


# How to "OVERRIDE/MODIFY" fields from a common base?


# How to "REMOVE" fields from a common base?
##  SEE https://github.com/samuelcolvin/pydantic/issues/1460


# form openapi-generator