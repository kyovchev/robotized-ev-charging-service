import asyncio
import websockets

async def loop():
    uri = "ws://0.0.0.0:8999"
    try:
        async with websockets.connect(uri) as websocket:
            while True:
                try:
                    name = input("> ")
                    await websocket.send(name)
                    response = await websocket.recv()
                    print(response)
                except:
                    print("Error: Socket is closed!")
                    break
    except:
        print("Error: Server is not active!")

if __name__ == "__main__":
    asyncio.run(loop())
