# Sample provided by Mark Arnold with small changes to adapt it

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
            # awaits for new inputs
            input_1 = await (await PORTS.inputs)[0].get()
            x = float(input_1.read_text())
        except:
            # commands a reset => exception
            x = 0

        # PM run
        y = x + 0.5
        print("y=" + str(y) + "x=" + str(x))

        # dump result in output
        p.write_text(str(y))
        await (await PORTS.outputs)[0].set(p)

    p.write_text("0")
    await (await PORTS.outputs)[0].set(p)


async def main_v2():
    @output(1)
    def add_half(x):
        return x + 0.5

    x = 0
    while x < 10:
        async for x in get("x"):
            y = add_half(x)


if __name__ == "__main__":
    asyncio.run(main())
