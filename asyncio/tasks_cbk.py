import asyncio


async def foo():
    await asyncio.sleep(1)
    return "Foo!"


async def hello_world():
    task = asyncio.create_task(foo())

    def got_result(future):
        assert future is task
        print(f"got the result! {future.result()}")

    task.add_done_callback(got_result)
    print(task)
    await asyncio.sleep(1)
    print("Hello World!")
    await asyncio.sleep(1)
    print(task)


asyncio.run(hello_world())