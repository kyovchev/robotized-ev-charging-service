import asyncio
from datetime import datetime
import websockets
from ocpp.routing import on
from ocpp.v16 import ChargePoint as cp
from ocpp.v16.enums import *
from ocpp.v16 import call_result, call
import time

import config

class ChargePoint(cp):
    def __init__(self, id, connection):
        response_timeout = 3
        super().__init__(id, connection, response_timeout)

    @on(Action.BootNotification)
    def on_boot_notification(
        self, charge_point_vendor: str, charge_point_model: str, **kwargs
    ):
        return call_result.BootNotificationPayload(
            current_time=datetime.utcnow().isoformat(),
            interval=10,
            status=RegistrationStatus.accepted,
        )

    @on(Action.Heartbeat)
    def on_heartbeat(self):
        return call_result.HeartbeatPayload(
            current_time=datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S") + "Z"
        )
    
    @on(Action.Authorize)
    def on_authorize(self, id_tag):
        return call_result.AuthorizePayload(
            id_tag_info={
                "status": 'Accepted'
            }
        )

    @on(Action.StartTransaction)
    def on_start_transaction(self, connector_id, id_tag, timestamp, meter_start, reservation_id):
        return call_result.StartTransactionPayload(
            id_tag_info={
                "status": "Accepted"
            },
            transaction_id=int(1)
        )

    @on(Action.StopTransaction)
    def on_stop_transaction(self, transaction_id, id_tag, timestamp, meter_stop, reason):
        return call_result.StopTransactionPayload(
            id_tag_info={
                "status": 'Accepted'
            }
        )
    
    @on(Action.MeterValues)
    def on_meter_value(self, connector_id, meter_value, transaction_id):
        return call_result.MeterValuesPayload()

    @on(Action.StatusNotification)
    def on_status_notification(self, connector_id, error_code, info, status, timestamp):
        print(f'StatusNotification: {status}')
        return call_result.StatusNotificationPayload()

    async def remote_start_transaction(self):
        request = call.RemoteStartTransactionPayload(
            id_tag="1",
            connector_id=1
        )
        response = await self.call(request)
        if response.status == RemoteStartStopStatus.accepted:
            print("Transaction Started!")

    async def remote_stop_transaction(self):
        request = call.RemoteStopTransactionPayload(
            transaction_id=1
        )
        response = await self.call(request)
        if response.status == RemoteStartStopStatus.accepted:
            print("Stopping transaction")

async def on_connect(websocket, path):
    try:
        requested_protocols = websocket.request_headers["Sec-WebSocket-Protocol"]
    except KeyError:
        print("Error: Client hasn't requested any Subprotocol. Closing Connection!")
        return await websocket.close()
    if websocket.subprotocol:
        print(f'Protocols Matched: {websocket.subprotocol}')
    else:

        print(f'Protocols Mismatched | Expected Subprotocols: {websocket.available_subprotocols}, \
                but client supports  {requested_protocols} | Closing connection!')
        return await websocket.close()

    charge_point_id = path.strip("/")
    cp = ChargePoint(charge_point_id, websocket)

    await cp.start()

connected = set()
clients = dict()
ping_counter = 0
clients_couter = 0

@asyncio.coroutine
async def on_connect(websocket, path):
    charge_point_id = path.strip('/')
    cp = ChargePoint(charge_point_id, websocket)
    try:
        await asyncio.gather(cp.start(), register(websocket, path))
    except websockets.exceptions.ConnectionClosed:
        connected.remove(websocket)
        print("Charge Point disconnected!")

@asyncio.coroutine
async def register(websocket, path):
    await asyncio.sleep(2)
    connected.add(websocket)
    charge_point_id = path.strip('/')
    print(f'Register Charge Point {charge_point_id}')
    config.charging_point = ChargePoint(charge_point_id, websocket)
