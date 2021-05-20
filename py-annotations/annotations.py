
from inspect import signature
from pydantic import BaseSettings



def foo(a, *, b:int, **kwargs):
    pass


sig = signature(foo)
for param in sig.parameters.items():
    print(param.name)
    print(param.kind)
    print(param.annotation )