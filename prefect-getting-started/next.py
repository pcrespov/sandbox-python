from prefect import task, Flow
import prefect

def create_spark_cluster():
    return "some spark cluster"

def submit_job(cluster):
    print('submitted job to', cluster)

def tear_down(cluster):
    print('tearing down', cluster)

@task
def create_cluster():
    cluster = create_spark_cluster()
    return cluster

@task
def run_spark_job(cluster):
    submit_job(cluster)


# https://docs.prefect.io/core/getting_started/next-steps.html#triggers
@task(trigger=prefect.triggers.always_run)
def tear_down_cluster(cluster):
    tear_down(cluster)

from prefect.engine import signals

@task
def signal_task(message):
    if message == 'go!':
        raise signals.SUCCESS(message='going!')
    elif message == 'stop!':
        raise signals.FAIL(message='stopping!')
    elif message == 'skip!':
        raise signals.SKIP(message='skipping!')



with Flow("Spark2") as flow:
    # define data dependencies
    cluster = create_cluster()
    submitted = run_spark_job(cluster)
    result = tear_down_cluster(cluster)

    # https://docs.prefect.io/core/getting_started/next-steps.html#triggers
    # wait for the job to finish before tearing down the cluster
    result.set_upstream(submitted)

    ## https://docs.prefect.io/core/getting_started/next-steps.html#signals
    go = signal_task("go!")
    stop = signal_task("stop!")
    skip = signal_task("skip!")

    go.set_upstream(result)
    stop.set_upstream(result)
    skip.set_upstream(result)

    ## https://docs.prefect.io/core/getting_started/next-steps.html#reference-tasks
    flow.set_reference_tasks([submitted])


flow.register(project_name="test")
