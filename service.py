import asyncio
import websockets

from external_comm import external_comm
from central_system import on_connect

async def main():
    server1 = await websockets.serve(
        on_connect, "0.0.0.0", 9000, subprotocols=["ocpp1.6"]
    )
    server2 = await websockets.serve(
        external_comm, '0.0.0.0', 8999
    )
    await asyncio.gather(server1.wait_closed(), server2.wait_closed())

if __name__ == "__main__":
    asyncio.run(main())
