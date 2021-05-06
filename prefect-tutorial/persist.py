import prefect
from prefect import Flow, Task, task
from prefect.engine.results import LocalResult


class MyTask(Task):
    def run(self):
        return 42


result = LocalResult("./my-result")

# create a task via initializing our custom Task class
class_task = MyTask(checkpoint=True, result=LocalResult("./my-result"))


# create a task via the task decorator
@task(checkpoint=True, result=LocalResult("./my-result"))
def func_task(x):
    return 99 * x

@task
def report_start_day():
    logger = prefect.context.get("logger")
    logger.info(prefect.context.today)

with Flow("persist", result=result) as flow:
    report_start_day()
    x = class_task()
    y = func_task(x=x)


flow.run()

# Q??
# - Why nothing is saved into result????
