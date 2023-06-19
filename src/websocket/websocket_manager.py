import json
from fastapi import WebSocket


class ConnectionManager:
    def __init__(self):
        self.active_connections: list[WebSocket] = []

    async def connect(self, ws: WebSocket):
        await ws.accept()
        self.active_connections.append(ws)

    def disconnect(self, ws: WebSocket):
        self.active_connections.remove(ws)

    async def send_data(self, data, ws: WebSocket):
        await ws.send_json(data)

    async def broadcast(self, message: str):
        for connection in self.active_connections:
            await connection.send_json(json.dumps({'message': 'person disconect'}))
