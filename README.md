# Robotized EV Charging Service

The `service.py` serves two websocket servers.

The server at port 9000 is used for connection to EV Charge Point through Open Charge Point Protocol (OCPP) 1.6. It requires the [OCPP Python library](https://github.com/mobilityhouse/ocpp).

The server at port 8999 is used for connection to an external communication service. For example, this [web-based user interface](https://github.com/kyovchev/robotized-ev-charging-webui). The external service can send to the websocket the following commands:
- `start`: start charging;
- `stop`: stop charging.

The EV Charge Point can be simulated with the following [simulator](https://github.com/kyovchev/OCPP-1.6-Chargebox-Simulator).

The external communication can also be tested with the `external_comm.py`.

At this moment only *one* Charge Point is supported.
