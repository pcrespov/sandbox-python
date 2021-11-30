import json
from inspect import Signature, Parameter
from typing import OrderedDict, Union
import collections
import sys
from pathlib import Path

curdir = Path(sys.argv[0] if __name__ == "__main__" else __file__).resolve().parent

meta = json.loads((curdir / "metadata.json").read_text())


# build signature from meta ----------
# TODO: extend to more complex annotaitons with pydantic
type2annotation = {
    "string": str,
    "number": float,
}
annotations2type = {v: k for k, v in type2annotation.items()}

parameters = []
for name, param in meta["inputs"].items():
    p = Parameter(
        name=name,
        kind=Parameter.POSITIONAL_OR_KEYWORD,
        default=param.get("DefaultValue", Parameter.empty),
        annotation=type2annotation.get(param["type"], Parameter.empty),
    )
    parameters.append(p)

outputs = OrderedDict(
    (name, type2annotation[output["type"]]) for name, output in meta["outputs"].items()
)

output_types = tuple(outputs.values())

sig = Signature(
    parameters,
    return_annotation=OrderedDict[str, Union[output_types]]
    if output_types
    else Signature.empty,
)
print(sig)


# An now the reverse -----------------------------------
assert isinstance(sig, Signature)

got_meta = {}
got_meta["inputs"] = collections.OrderedDict()
for param in sig.parameters.values():
    input_ = {}

    if param.annotation != Parameter.empty:
        input_["type"] = annotations2type[param.annotation]

    if param.default != Parameter.empty:
        input_["defaultValue"] = param.default

    got_meta["inputs"][param.name] = input_

got_meta["outputs"] = collections.OrderedDict()

import typing

assert typing.get_origin(sig.return_annotation) is collections.OrderedDict
_, output_types = typing.get_args(sig.return_annotation)

if typing.get_origin(output_types) is Union:
    for n, type_ in typing.get_args(output_types):
        got_meta["outputs"][f"out_{n}"] = annotations2type[type_]
else:
    got_meta["outputs"]["out_0"] = annotations2type[output_types]

print("got_meta", "-" * 10)
print(json.dumps(got_meta, indent=2))
