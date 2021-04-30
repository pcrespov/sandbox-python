import json
import time

from prefect import Flow, Task, task


@task
def sleeper(delay: int = 1):
    print("...")
    time.sleep(delay)
    print("X")
    return delay


with Flow("sleepers a lot 3") as flow:

    s0 = [sleeper() for _ in range(3)]

    s1 = [sleeper() for _ in range(6)]
    for s1i in s1[:4]:
        s1i.set_upstream(s0[0])
    for s1j in s1[4:]:
        s1j.set_upstream(s0[1])

    s2 = [sleeper() for _ in range(4)]
    s2[0].set_upstream(s1[0])

    s2[1].set_upstream(s1[1])
    s2[1].set_upstream(s1[2])

    s2[2].set_upstream(s1[3])
    s2[2].set_upstream(s1[4])

    s2[3].set_upstream(s1[5])

    s3 = [sleeper() for _ in range(2)]

    s3[0].set_upstream(s2[0])
    s3[0].set_upstream(s2[1])

    s3[1].set_upstream(s2[2])
    s3[1].set_upstream(s2[3])

    s4 = [sleeper() for _ in range(1)]
    s4[0].set_upstream(s3[0])
    s4[0].set_upstream(s3[1])

    for i, si in enumerate([s0, s1, s2, s3, s4]):
        for j, sij in enumerate(si):
            sij.name = f"sleeper {i}{j}"

flow.visualize(filename="sleepers-flow", format="svg")

with open("sleepers-flow.json", "wt") as f:
    json.dump(flow.serialize(), f, indent=2)

flow.register(project_name="test")
# flow.run()


# Beginning Flow run for 'sleepers a lot'
# Task 'sleeper 01': Starting task run...
# Task 'sleeper 01': Finished task run for task with final state: 'Success'
# Task 'sleeper 15': Starting task run...
# Task 'sleeper 15': Finished task run for task with final state: 'Success'
# Task 'sleeper 23': Starting task run...
# Task 'sleeper 23': Finished task run for task with final state: 'Success'
# Task 'sleeper 00': Starting task run...
# Task 'sleeper 00': Finished task run for task with final state: 'Success'
# Task 'sleeper 10': Starting task run...
# Task 'sleeper 10': Finished task run for task with final state: 'Success'
# Task 'sleeper 12': Starting task run...
# Task 'sleeper 12': Finished task run for task with final state: 'Success'
# Task 'sleeper 14': Starting task run...
# Task 'sleeper 14': Finished task run for task with final state: 'Success'
# Task 'sleeper 11': Starting task run...
# Task 'sleeper 11': Finished task run for task with final state: 'Success'
# Task 'sleeper 13': Starting task run...
# Task 'sleeper 13': Finished task run for task with final state: 'Success'
# Task 'sleeper 20': Starting task run...
# Task 'sleeper 20': Finished task run for task with final state: 'Success'
# Task 'sleeper 21': Starting task run...
# Task 'sleeper 21': Finished task run for task with final state: 'Success'
# Task 'sleeper 30': Starting task run...
# Task 'sleeper 30': Finished task run for task with final state: 'Success'
# Task 'sleeper 22': Starting task run...
# Task 'sleeper 22': Finished task run for task with final state: 'Success'
# Task 'sleeper 31': Starting task run...
# Task 'sleeper 31': Finished task run for task with final state: 'Success'
# Task 'sleeper 40': Starting task run...
# Task 'sleeper 40': Finished task run for task with final state: 'Success'
# Flow run SUCCESS: all reference tasks succeeded
