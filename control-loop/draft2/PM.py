# Sample provided by Mark Arnold with small changes to adapt it
import asyncio
from pathlib import Path

from simcore_sdk import node_ports
import numpy as np


async def main():
    Nsim = 10
    PORTS = await node_ports.ports()
    init_simtime_u = "[0,np.array([0.0,0.0,0.0,0.0,0.0,0.0])]"
    init_simtime_ym = "[0,np.array([0.0,0.0])]"
    s = ""
    olds = ""
    simtime, u = eval(init_simtime_u)
    simtime, ym = eval(init_simtime_ym)
    while simtime < Nsim:
        while olds == s:
            try:
                input_1 = await (await PORTS.inputs)[0].get()
                s = input_1.read_text()
            except:
                s = init_simtime_u
        olds = s
        simtime, u = eval(s)
        ym = PM(u)
        p = Path("ym.dat")
        p.write_text("[" + str(simtime + 1) + ",np." + repr(ym) + "]")
        await (await PORTS.outputs)[0].set(p)
    p = Path("ym.dat")
    p.write_text(init_simtime_ym)
    await (await PORTS.outputs)[0].set(p)


if __name__ == "__main__":
    asyncio.run(main())
