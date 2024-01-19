import random


def zoo():
    raise TypeError

def foo(x):
    if x>0:
        raise ValueError

def bar():
    foo(random.randint(-10,10))


def file_stuff(path):
    return open(path)

def main():
    try:
        bar()
        zoo()
    except ValueError:
        file_stuff(".")



# python parse_exceptions.py script.py
#
# Function 'zoo' may raise the following exceptions: TypeError
# Function 'foo' may raise the following exceptions: ValueError
# Function 'bar' may raise the following exceptions: ValueError
# Function 'file_stuff' may raise the following exceptions: FileNotFoundError, PermissionError
# Function 'main' may raise the following exceptions: FileNotFoundError, TypeError, PermissionError
#
