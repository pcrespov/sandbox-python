# https://docs.python.org/3/whatsnew/3.8.html


# https://docs.python.org/3/whatsnew/3.8.html#positional-only-parameters

#%% https://docs.python.org/3/whatsnew/3.8.html#assignment-expressions
a = list(range(5))

if ( n:= len(a) ) > 2:
    print(n)


#
# https://docs.python.org/3/whatsnew/3.8.html#positional-only-parameters


# %%
import re

if (m := re.search( r"(o+)", "foo this is good") ) :
    print(m.groups())


# %%
def f(a, b, /, c, d, *, e, f):
    print(a,b,c,d,e,f)

f(3,4,5,d=6, e=7, f=8)

#
# https://docs.python.org/3/whatsnew/3.8.html#f-strings-support-for-self-documenting-expressions-and-debugging
#
# %%
x = 33
print(f"{x=} and {x/2=}")

# %%
def parse(family):
    lastname, *members = family.split()
    return lastname.upper(), *members

parse('simpsons homer marge bart lisa maggie')



## sigle-dispatch generic function

# %%
from functools import singledispatch, singledispatchmethod

@singledispatch
def fun(a, b=False):
    return a, b


@fun.register
def _(a: int, b=False):
    return "int", a, b


print(fun(33.33))
print(fun(2))
print(fun("foo"))


class Negator:
    @singledispatchmethod
    def neg(self, arg):
        raise NotImplementedError("Cannot negate a")

    @neg.register
    def _(self, arg: int):
        return -arg

    @neg.register
    def _(self, arg: bool):
        return not arg

print(Negator().neg(33))
print(Negator().neg(False))
# %%
