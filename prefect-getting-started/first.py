from prefect import task
from prefect import Task


# decorator produces task object
@task
def say_hello(person: str) -> None:
    print("Hello, {}!".format(person))


@task
def add(x, y=1):
    return x + y


class AddTask(Task):
    def __init__(self, default: int, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.default = default

    def run(self, x: int, y: int = None) -> int:
        if y is None:
            y = self.default
        return x + y


# initialize the task instance
add_instance = AddTask(default=1)

assert isinstance(add_instance, Task)
assert isinstance(add, Task)
assert isinstance(say_hello, Task)

from typing import Union
from prefect.engine.state import State



## FUNCTIONAL API ------------
from prefect import Flow

with Flow("My first flow!") as flow:
    first_result = add(1, y=2)
    assert isinstance(first_result, Task)

    second_result = add(x=first_result, y=100)
    assert isinstance(second_result, Task)

    # graph created at this point

    state: Union[State, None] = flow.run()

    assert state.is_successful()

    first_task_state = state.result[first_result]
    assert first_task_state.is_successful()
    assert first_task_state.result == 3

    second_task_state = state.result[second_result]
    assert second_task_state.is_successful()
    assert second_task_state.result == 103


from prefect import Parameter

with Flow("Say hi!") as flow:
    name = Parameter("name")
    say_hello(name)

    flow.run(name="pedro")


## IMPERATIVE API ----------
if False:
    flow = Flow("imperative flow")

    # tasks
    name = Parameter("name")
    second_add = add.copy()


    flow.add_task(add)
    flow.add_task(second_add)
    flow.add_task(say_hello)

    # create NON-DATA dependencies so that `say_hello` waits for `second_add` to finish 
    say_hello.set_upstream(second_add, flow=flow)


    # create data bindings (i.e. DATA)
    add.bind(x=1, y=2, flow=flow)
    second_add.bind(x=add, y=100, flow=flow) # creates DATA dependencies

    with flow:
        say_hello(name)

        flow.run(name="bar")


#flow.register(project_name="test")

# In [14]: !prefect create project 'test'
# test created

# In [15]: flow.register(project_name="test")
# Flow URL: http://localhost:8080/default/flow/5ac32127-5f4d-4d28-b5f9-fd90ccb6cfa3
#  └── ID: d48d2f6f-1915-4a02-bcfe-773119ae3915
#  └── Project: test
#  └── Labels: ['crespo-wkstn']
# Out[15]: 'd48d2f6f-1915-4a02-bcfe-773119ae3915'