import uvicorn
from typing import AsyncGenerator
from fastapi import FastAPI, Request, HTTPException, Depends, status, WebSocket, WebSocketDisconnect
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.responses import JSONResponse
from db.queries import write_opinion
from chat import ConnectionManager
from contextlib import asynccontextmanager
from typing import Dict, List
import uuid

from config import settings
from db import init_db
from auth import (
    authenticate_user,
    create_access_token,
    get_current_active_user
)
from utils import (setup_logger,
                   logs,
                   ModelReadiness,
                   TextRequest,
                   RankingPairRequest,
                   NSFWRequest,
                   Token,
                   TokenData,
                   User,
                   UserInDB
)


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
   await init_db()
   yield


app = FastAPI(lifespan=lifespan)


manager = ConnectionManager()


@logs
@app.post("/auth", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = await authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = create_access_token(data={"sub": user.email})
    return {"access_token": access_token, "token_type": "bearer"}


@app.get("me/", response_model=User)
async def read_users_me(current_user: User = Depends(get_current_active_user)):
    return current_user


@app.get("/regions", response_model=List[str])
async def get_all_regions():
    async with get_session() as session:
        result = await session.exec(select(Region.title))
        return result.all()
    

@app.get("/regions/{region_title}/cities", response_model=List[str])
async def get_cities_by_region(region_title: str):
    async with get_session() as session:
        region_result = await session.exec(select(Region).where(Region.title == region_title))
        region = region_result.first()

        if not region:
            raise HTTPException(status_code=404, detail="Регион не найден")

        cities_result = await session.exec(
            select(Locality.name).where(Locality.region_id == region.id)
        )
        return cities_result.all()


@app.websocket("/chat/{user_id_req}/{user_id_rep}/{opinion}")
async def chat(websocket: WebSocket, user_id_req: int, user_id_rep: int, opinion: bool):
    # Используем write_opinion как проверку
    matched, match = await write_opinion(user_id_req, user_id_rep, opinion)

    if not matched:
        # Если нет match — закрываем соединение
        await websocket.close(code=1008)  # Policy Violation
        return

    # Если есть Match — подключаем к чату
    await manager.connect(websocket, user_id_req, user_id_rep)

    try:
        while True:
            data = await websocket.receive_text()
            await manager.send_personal_message(user_id_req, user_id_rep, data)
    except WebSocketDisconnect:
        manager.disconnect(user_id_req, user_id_rep)


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


#TODO MOVE route
# @app.get("/")
# async def get(request: Request):
#     return {"request": request}

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
    host, port = settings.back_api.split(':')
    uvicorn.run("main:app", host=host, port=int(port), reload=True)
