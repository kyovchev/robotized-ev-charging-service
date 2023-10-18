import config
import websockets
from asyncio.exceptions import TimeoutError

async def external_comm(websocket):
    print("External service is connected.")
    while True:
        if websocket:
            try:
                command = await websocket.recv()
            except:
                print("Error: Cannot receive from the socket!")
                break
        
            response = "?"

            if command == "start":
                print("Start charging.")
                try:
                    await config.charging_point.remote_start_transaction()
                    response = "Charging is started..."
                except TimeoutError:
                    response = "Charging is started."
                except:
                    print("Error: Cannot send start command!")
                    response = "Error: Cannot sent start command!"
            elif command == "stop":
                print("Stop charging.")
                try:
                    await config.charging_point.remote_stop_transaction()
                    response = "Charging is stopped."
                except TimeoutError:
                    response = "Charging is stopped."
                except:
                    print("Error: Cannot send stop command!")
                    response = "Error: Cannot sent stop command!"
            elif command == "exit":
                print("Closing the socket.")
                break
            else:
                response = "?"
                print(f'Error: Unknown command {command}!')

            try:
                await websocket.send(response)
            except:
                print("Error: Cannot respond to the socket!")
                break
        else:
            print("Error: Socket is not active!")
            break
