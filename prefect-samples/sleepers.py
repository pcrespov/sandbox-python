import time
from prefect import task, Flow, Task


@task
def sleeper(delay: int=1):
    print("Sleeping %s secs", delay)
    time.sleep(delay)
    print("Slept %s secs", delay)
    return delay




with Flow("sleepers a lot") as flow:
    s0 = [ sleeper() for _ in range(2) ]

    s1 = [ sleeper() for _ in range(6) ]
    for s1i in s1[:4]:
        s1i.set_upstream(s0[0])
    for s1j in s1[4:]:
        s1j.set_upstream(s0[1])

    s2 = [ sleeper() for _ in range(4) ]
    s2[0].set_upstream(s1[0])
    
    s2[1].set_upstream(s1[1])
    s2[1].set_upstream(s1[2])

    s2[2].set_upstream(s1[3])
    s2[2].set_upstream(s1[4])

    s2[3].set_upstream(s1[5])

    s3 = [ sleeper() for _ in range(2) ]

    s3[0].set_upstream(s2[0])
    s3[0].set_upstream(s2[1])

    s3[1].set_upstream(s2[2])
    s3[1].set_upstream(s2[3])


    s4 = [ sleeper() for _ in range(1) ]
    s4[0].set_upstream(s3[0])
    s4[0].set_upstream(s3[1])


    for i, si in enumerate( [s0,s1,s2,s3,s4] ):
        for j, sij in enumerate(si):
            sij.name = f"sleeper {i}{j}"

flow.visualize(filename="sleepers-flow", format="svg")
#flow.register(project_name="tests")