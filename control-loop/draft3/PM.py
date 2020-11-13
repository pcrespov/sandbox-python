# Sample provided by Mark Arnold with small changes to adapt it
import asyncio
import time
from pathlib import Path

import numpy as np
from simcore_sdk import node_ports


def PM(u):
    pass


async def main():
    Nsim = 10
    init_simtime_u = "[0,np.array([0.0,0.0,0.0,0.0,0.0,0.0])]"
    init_simtime_ym = "[0,np.array([0.0,0.0])]"
    s = ""
    olds = ""
    simtime, u = eval(init_simtime_u)
    simtime, ym = eval(init_simtime_ym)
    while simtime < Nsim:
        while olds == s:
            try:
                input_1 = open(Path("u.dat"))
                s = input_1.read()
            except:
                s = init_simtime_u
            time.sleep(1)
        olds = s
        simtime, u = eval(s)
        ym = PM(u)
        p = Path("ym.dat")
        output1 = open(p, "w")
        output1.write("[" + str(simtime + 1) + ",np." + repr(ym) + "]")


if __name__ == "__main__":
    asyncio.run(main())
