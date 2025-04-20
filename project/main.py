import uvicorn
from typing import AsyncGenerator
from fastapi import FastAPI, Request, HTTPException, Depends, status
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from config import settings
from db import init_db
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
