from typing import Optional

from prefect import Flow, Task, task, Parameter
from prefect.engine.state import State

# sparation of tasks ------------

@task
def say_hello(person: str) -> None:
    print(f"Hello, world {person}!")


@task
def add(x, y=1):
    return x + y


class AddTask(Task):
    def __init__(self, default):
        self.default = default

    def run(self, x, y: Optional[int] = None):
        if y is None:
            y = self.default
        return x + y

# initialize the task instance
add2 = AddTask(default=1)



# Defines workflow-----
with Flow("my first workflow") as flow:
    name = Parameter("name")

    first_result = add(1, y=2)
    second_result = add(x=first_result, y=100)

    say_hello(person=name, upstream_tasks=[second_result])
    # OR say_hello.set_upstream(second_result)

flow.visualize()
flow.register(project_name="foo")


def main():
    # Execution
    state: State = flow.run(name="pcrespov")

    assert state.is_successful()

    first_task_state = state.result[first_result]
    assert first_task_state.is_successful()
    assert first_task_state.result == 3

    second_task_state = state.result[second_result]
    assert second_task_state.is_successful()
    assert second_task_state.result == 103
