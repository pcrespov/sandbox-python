import random


def foo(x):
    if x>0:
        raise ValueError

def bar():
    foo(random.randint(-10,10))


def main():
    bar()