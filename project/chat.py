from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from typing import Dict, Tuple
from db import get_matches

router = APIRouter()


@router.websocket("/ws/{user_id}/{target_id}")
async def chat(websocket: WebSocket, user_id: int, target_id: int):
    await manager.connect(websocket, user_id, target_id)
    try:
        while True:
            data = await websocket.receive_text()
            await manager.send_personal_message(user_id, target_id, data)
    except WebSocketDisconnect:
        manager.disconnect(user_id, target_id)


class ConnectionManager:
    def __init__(self):
        self.active_connections: Dict[Tuple[int, int], Dict[int, WebSocket]] = {}

    def _get_chat_key(self, user1: int, user2: int):
        return tuple(sorted([user1, user2]))

    async def connect(self, websocket: WebSocket, user_id: int, target_id: int):
        matches = await get_matches(user_id)
        if target_id not in matches:
            await websocket.close(code=4003, reason="No match between users")
            return

        await websocket.accept()
        key = self._get_chat_key(user_id, target_id)
        if key not in self.active_connections:
            self.active_connections[key] = {}
        self.active_connections[key][user_id] = websocket

    def disconnect(self, user_id: int, target_id: int):
        key = self._get_chat_key(user_id, target_id)
        if key in self.active_connections and user_id in self.active_connections[key]:
            del self.active_connections[key][user_id]
            if not self.active_connections[key]:
                del self.active_connections[key]

    async def send_personal_message(self, sender_id: int, receiver_id: int, message: str):
        key = self._get_chat_key(sender_id, receiver_id)
        connections = self.active_connections.get(key, {})
        for uid, conn in connections.items():
            await conn.send_text(f"{sender_id}: {message}")

    async def get_user_active_connections(self, user_id: int):
        matches = await get_matches(user_id)
        active_chats = []
        
        for match_id in matches:
            key = self._get_chat_key(user_id, match_id)
            if key in self.active_connections and user_id in self.active_connections[key]:
                active_chats.append({
                    "target_id": match_id,
                    "connection": self.active_connections[key][user_id]
                })
        
        return active_chats


manager = ConnectionManager()
