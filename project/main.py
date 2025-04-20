import uvicorn
from fastapi import FastAPI, Request, HTTPException, Depends, status, WebSocket, WebSocketDisconnect
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from fastapi.security import OAuth2PasswordRequestForm
from chat import ConnectionManager
from typing import Dict, List, AsyncGenerator
import uuid

from config import settings
from db import init_db, write_opinion, get_regions, get_cities_by_region_name, get_bad_habits, get_interests, get_educ_dir
from chat import router as chat_router
from auth import router as auth_router
from auth import (
    authenticate_user,
    create_access_token,
    get_current_active_user
)

from utils import (
    setup_logger,
    logs,
    ModelReadiness,
    TextRequest,
    RankingPairRequest,
    NSFWRequest,
    Token,
    TokenData,
    UserData,
    UserAuth
)

manager = ConnectionManager()

@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
   await init_db()
   yield


app = FastAPI(
    lifespan=lifespan,
    docs_url="/api/docs",
    redoc_url="/api/redoc",
    openapi_url="/api/openapi.json"
)

app.add_middleware(
    CORSMiddleware,
    #allow_origins=settings.allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

app.include_router(auth_router, prefix="/api")
app.include_router(chat_router, prefix="/api/chat", tags=["chat"])


@app.get("/get_regions", response_model=List[str])
async def get_all_regions():
    return get_regions()
    

@app.get("/get_regions/{region_title}/cities", response_model=List[str])
async def get_cities_by_region(region_title: str):
    return get_cities_by_region_name(region_title)


@app.get("/get_bad_habits", response_model=List[str])
async def get_all_bad_habits():
    return get_bad_habits()


@app.get("/get_interests", response_model=List[str])
async def get_all_interests():
    return get_all_interests()


@app.get("/get_educ_dir", response_model=List[str])
async def get_all_educ_dir():
    return get_educ_dir()


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


if __name__ == '__main__':
    setup_logger()
    host, port = settings.back_api.split(':')
    uvicorn.run("main:app", host=host, port=int(port), reload=True)
