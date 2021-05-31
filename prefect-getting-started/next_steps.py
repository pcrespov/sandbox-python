# https://docs.prefect.io/core/getting_started/next-steps.html

import prefect
from prefect import Flow, task
from prefect.engine import signals


@task
def setup():
    return "cluster"


@task
def evaluate(cluster):
    return f"evaluation of {cluster}"


@task(trigger=prefect.triggers.always_run)
def cleanup(cluster):
    print(f"cleaning up {cluster}")


_runs = 0

@task
def signal_task(message):
    #
    # fine-grain controls over the task
    # state by raising exceptions called signals
    #
    global _runs

    if message == "go!":
        raise signals.SUCCESS(message="going!")
    elif message == "stop!":
        raise signals.FAIL(message="stopping!")
    elif message == "skip!":
        raise signals.SKIP(message="skipping!")
    elif message == "retry!":
        _runs += 1
        if _runs == 1:
            raise signals.RETRY(message="le'ts try again!")
    elif message == "pause!":
        _runs += 1
        if _runs == 2:
            raise signals.PAUSE(message="let's take a break!")
    
    raise signals.SUCCESS(message="going!")


with Flow("setup-eval-cleanup-flow") as flow:
    # define data dependencies
    cluster = setup()
    submitted = evaluate(cluster)
    teardown = cleanup(cluster)

    # adds a non-data upstream dependency
    # so that cleanup is done when evaluation is finished
    # even if the latter does not pass results
    teardown.set_upstream(submitted)


    # add extra tasks and that trigger different states
    go = signal_task("go!")
    go.set_upstream(teardown)
    
    stop=signal_task("stop!")
    stop.set_upstream(teardown)
    
    skip=signal_task("skip!")
    skip.set_upstream(teardown)
    
    retry=signal_task("retry!")
    retry.set_upstream(teardown)

    pause = signal_task("pause!")
    pause.set_upstream(teardown)

    ## https://docs.prefect.io/core/getting_started/next-steps.html#reference-tasks
    flow.set_reference_tasks([submitted])


flow.run()
# flow.register(project_name="test")

# INFO - prefect.FlowRunner | Beginning Flow run for 'setup-eval-cleanup-flow'
# INFO - prefect.TaskRunner | Task 'setup': Starting task run...
# INFO - prefect.TaskRunner | Task 'setup': Finished task run for task with final state: 'Success'
# INFO - prefect.TaskRunner | Task 'evaluate': Starting task run...
# INFO - prefect.TaskRunner | Task 'evaluate': Finished task run for task with final state: 'Success'
# INFO - prefect.TaskRunner | Task 'cleanup': Starting task run...
# cleaning up cluster
# INFO - prefect.TaskRunner | Task 'cleanup': Finished task run for task with final state: 'Success'


# INFO - prefect.TaskRunner | Task 'signal_task': Starting task run...
# INFO - prefect.TaskRunner | SUCCESS signal raised: SUCCESS('going!')
# INFO - prefect.TaskRunner | Task 'signal_task': Finished task run for task with final state: 'Success'
# INFO - prefect.TaskRunner | Task 'signal_task': Starting task run...
# INFO - prefect.TaskRunner | SKIP signal raised: SKIP('skipping!')
# INFO - prefect.TaskRunner | Task 'signal_task': Finished task run for task with final state: 'Skipped'
# INFO - prefect.TaskRunner | Task 'signal_task': Starting task run...
# INFO - prefect.TaskRunner | RETRY signal raised: RETRY("le'ts try again!")
# INFO - prefect.TaskRunner | Task 'signal_task': Finished task run for task with final state: 'Retrying'
# INFO - prefect.TaskRunner | Task 'signal_task': Starting task run...
# INFO - prefect.TaskRunner | PAUSE signal raised: PAUSE("let's take a break!")
# INFO - prefect.TaskRunner | Task 'signal_task': Finished task run for task with final state: 'Paused'
# INFO - prefect.TaskRunner | Task 'signal_task': Starting task run...
# INFO - prefect.TaskRunner | FAIL signal raised: FAIL('stopping!')
# INFO - prefect.TaskRunner | Task 'signal_task': Finished task run for task with final state: 'Failed'
# INFO - prefect.FlowRunner | Flow run RUNNING: terminal tasks are incomplete.
# <Task: signal_task> is currently Paused; enter 'y' to resume:
# y
# INFO - prefect.FlowRunner | Beginning Flow run for 'setup-eval-cleanup-flow'
# INFO - prefect.TaskRunner | Task 'signal_task': Starting task run...
# INFO - prefect.TaskRunner | SUCCESS signal raised: SUCCESS('going!')
# INFO - prefect.TaskRunner | Task 'signal_task': Finished task run for task with final state: 'Success'
# INFO - prefect.TaskRunner | Task 'signal_task': Starting task run...
# INFO - prefect.TaskRunner | SUCCESS signal raised: SUCCESS('going!')
# INFO - prefect.TaskRunner | Task 'signal_task': Finished task run for task with final state: 'Success'


# INFO - prefect.FlowRunner | Flow run SUCCESS: all reference tasks succeeded
