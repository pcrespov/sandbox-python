# Sample provided by Mark Arnold with small changes to adapt it

# this code is in the control node
import asyncio
from pathlib import Path

from simcore_sdk import node_ports


async def main():
    p = Path("x.dat")
    PORTS = await node_ports.ports()

    x = 0
    while x < 10:
        try:
            input_1 = await (await PORTS.inputs)[0].get()
            y = float(input_1.read_text())
        except:
            y = 0

        x = y + 1
        print("x=" + str(x) + "y=" + str(y))

        p.write_text(str(x))
        await (await PORTS.outputs)[0].set(p)

    p.write_text("0")
    await (await PORTS.outputs)[0].set(p)


if __name__ == "__main__":
    asyncio.run(main())
