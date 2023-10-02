from pydantic import BaseModel, StrictStr, constr, parse_obj_as

OSPARC_IDENTIFIER_PREFIX = "FOO"


class OsparcVariableIdentifier(BaseModel):
    __root__: constr(regex=rf"^\${{?{OSPARC_IDENTIFIER_PREFIX}[A-Za-z0-9_]+}}?(:-.+)?$")


m1 = OsparcVariableIdentifier(__root__="$FOO_1234")
m2 = OsparcVariableIdentifier.parse_obj("$FOO_1234")
m3 = parse_obj_as(OsparcVariableIdentifier, "$FOO_1234")

m4 = parse_obj_as(
    constr(regex=rf"^\${{?{OSPARC_IDENTIFIER_PREFIX}[A-Za-z0-9_]+}}?(:-.+)?$"), "$FOO_1"
)

print(m1)


m5 = parse_obj_as(OsparcVariableIdentifier | str, "$FOO_1234")
m6 = parse_obj_as(OsparcVariableIdentifier | StrictStr, "FOO_1234")
