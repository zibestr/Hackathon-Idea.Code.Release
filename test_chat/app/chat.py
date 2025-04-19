from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Depends
from .ws_manager import ConnectionManager

manager = ConnectionManager()
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

