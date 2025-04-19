import uvicorn
from typing import AsyncGenerator
from fastapi import FastAPI, Request, HTTPException, WebSocket, WebSocketDisconnect
from fastapi.responses import JSONResponse
from fastapi.templating import Jinja2Templates
from contextlib import asynccontextmanager
from typing import Dict
import uuid

from config import settings
from utils import setup_logger, logs
#from db import create_models, init_db, get_session

templates = Jinja2Templates(directory="templates")
#@asynccontextmanager
#async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
#    await init_db()
#    yield


#app = FastAPI(lifespan=lifespan)
app = FastAPI()

class ConnectionManager:
    def __init__(self):
        self.active_connections: Dict[str, WebSocket] = {}
        self.usernames: Dict[str, str] = {}  # {user_id: username}

    async def connect(self, websocket: WebSocket, user_id: str):
        await websocket.accept()
        self.active_connections[user_id] = websocket

    async def register_user(self, user_id: str, username: str):
        self.usernames[user_id] = username
        print("{} Онлайн".format(username))

    async def disconnect(self, user_id: str):
        if user_id in self.usernames:
            username = self.usernames[user_id]
            del self.active_connections[user_id]
            del self.usernames[user_id]
            print("{} не онлайн".format(username))

    async def broadcast(self, message: str):
        for connection in self.active_connections.values():
            await connection.send_text(message)

manager = ConnectionManager()


@logs
@app.exception_handler(HTTPException)
async def app_exception_handler(request: Request, exc: HTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": {
                "code": exc.detail.get("code") if isinstance(exc.detail, dict) else "error",
                "message": exc.detail.get("message") if isinstance(exc.detail, dict) else exc.detail,
            }
        },
    )


@app.get("/")
async def get(request: Request):
    return templates.TemplateResponse("chat.html", {"request": request})

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    user_id = str(uuid.uuid4())
    await manager.connect(websocket, user_id)
    
    try:
        username = await websocket.receive_text()
        await manager.register_user(user_id, username)
        
        while True:
            message = await websocket.receive_text()
            await manager.broadcast(f"{username}: {message}")
            
    except WebSocketDisconnect:
        await manager.disconnect(user_id)
    except Exception as e:
        print(f"Ошибка: {e}")
        await manager.disconnect(user_id)




if __name__ == '__main__':
    setup_logger()
    uvicorn.run("main:app", host="0.0.0.0", port=settings.port, reload=True)
