# Sample provided by Mark Arnold with small changes to adapt it
import asyncio
import time
from pathlib import Path

from simcore_sdk import node_ports
import numpy as np


def controller(y):
    pass


async def main():
    Nsim = 10
    init_simtime_u = "[0,np.array([0.0,0.0,0.0,0.0,0.0,0.0])]"
    init_simtime_ym = "[0,np.array([0.0,0.0])]"
    s = ""
    olds = ""
    simtime, u = eval(init_simtime_u)
    while simtime < Nsim:
        while olds == s:
            try:
                input_1 = open(Path("ym.dat"))  # maybe in a dir somewhere
                s = input_1.read()
            except:
                s = init_simtime_ym
            time.sleep(1)
        olds = s
        simtime, ym = eval(s)
        u = controller(ym)
        p = Path("u.dat")
        output1 = open(p, "w")
        output1.write("[" + str(simtime) + ",np." + repr(u) + "]")


if __name__ == "__main__":
    asyncio.run(main())
