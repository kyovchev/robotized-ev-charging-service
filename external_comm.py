import config
import websockets
from asyncio.exceptions import TimeoutError

async def external_comm(websocket):
    print("External service is connected.")
    while True:
        if websocket:
            try:
                command = await websocket.recv()
                print(command)
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
                    response = "Error: Cannot send start command!"
            elif command == "stop":
                print("Stop charging.")
                try:
                    await config.charging_point.remote_stop_transaction()
                    response = "Charging is stopped."
                except TimeoutError:
                    response = "Charging is stopped."
                except:
                    print("Error: Cannot send stop command!")
                    response = "Error: Cannot send stop command!"
            elif command == "status":
                print("Request status.")
                try:
                    response = f'Status: {config.status}, transaction_id: {config.transaction_id}, meter_value: {config.meter_value}'
                except TimeoutError:
                    response = "Cannot retrieve status!"
                except:
                    print("Error: Cannot retrieve status.")
                    response = "Error: Cannot retrieve status!"
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
