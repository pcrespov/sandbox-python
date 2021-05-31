import asyncio

async def coro(n=1):
    await asyncio.sleep(n)
    return 3

    

class Foo:
    def bar(self):
        return 3

    def zee(self):
        return 7



def some_func_using_Foo():
    foo = Foo()
    print("bar", foo.bar())
    print("zee", foo.zee())
    return foo.bar()
