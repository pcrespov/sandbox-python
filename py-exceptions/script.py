import random


def foo(x):
    if x>0:
        raise ValueError

def bar():
    foo(random.randint(-10,10))


def main():
    try:
        bar()
    except ValueError:
        ...


# `python parse_exceptions.py script.py`
#
# Function 'foo' may raise the following exceptions: ValueError
# Function 'bar' may raise the following exceptions: None
# Function 'main' may raise the following exceptions: None

