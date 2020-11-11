# this code is in the PM node

import asyncio
from pathlib import Path

from simcore_sdk import node_ports

async def main():
    p = Path("y.dat")
    PORTS = await node_ports.ports()

    x = 0
    while x < 10:
        try:
            input_1 = await (await PORTS.inputs)[0].get()
            x = float(input_1.read_text())
        except:
            x = 0
        
        y = x + 0.5
        print("y=" + str(y) + "x=" + str(x))
        
        p.write_text(str(y))
        await (await PORTS.outputs)[0].set(p)

    p.write_text("0")
    await (await PORTS.outputs)[0].set(p)


if __name__ == "__main__":
    asyncio.run(main())
