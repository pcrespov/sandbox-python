import warnings
def foo():
    print('foo')
    warnings.warn("deprecated foo", FutureWarning)

def bar():
    print('bar')
    warnings.warn("deprecated bar ", FutureWarning)
