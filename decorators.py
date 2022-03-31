_registry = {}


def register(name: str):

    def decorator(func):
        assert name not in _registry
        _registry[name] = func
        return func
    return decorator


@register("foo")
def foo():
    print('running foo')

@register("bar")
def bar():
    print("running bar")


print(_registry)
foo()
foo()
bar()
print(_registry)
