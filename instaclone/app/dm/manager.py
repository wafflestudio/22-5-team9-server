from typing import Dict, List
from fastapi import WebSocket

from instaclone.app.dm.errors import ConnectionNotFoundError

class DMManager:
    def __init__(self) -> None:
        #manage connection from user id
        self.active_connections: Dict[int, WebSocket] = {}

    async def connect(self, user_id: int, websocket: WebSocket):
        await websocket.accept()
        self.active_connections[user_id] = websocket

    def disconnect(self, user_id: int):
        if user_id not in self.active_connections:
            raise ConnectionNotFoundError()
        else:
            del self.active_connections[user_id]
        
    async def send_personal_message(self, text: str, sender_id: int, receiver_id: int):
        if receiver_id in self.active_connections:
            websocket = self.active_connections[receiver_id]
            data = {
                "sender_id": sender_id,
                "receiver_id": receiver_id,
                "text": text
            }
            await websocket.send_json(data)