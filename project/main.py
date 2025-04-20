import uvicorn
from fastapi import FastAPI, Request, HTTPException, Depends, status, WebSocket, WebSocketDisconnect
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from fastapi.security import OAuth2PasswordRequestForm
from chat import ConnectionManager
from typing import Dict, List, AsyncGenerator
from config import settings
from db import init_db, write_opinion, get_regions, get_cities_by_region_name, get_bad_habits, get_interests, get_educ_dir
from chat import router as chat_router
from auth import router as auth_router
from auth import (
    authenticate_user,
    create_access_token,
    get_current_active_user
)

from db import (
    init_db,
    get_user_by_email,
    create_user,
    get_regions,
    get_cities_by_region_name,
    get_bad_habits,
    get_interests,
    get_educ_dir,
    update_user,
    check_password,
    get_recommendations,
    cache_recomendations,
    get_habitation,
    create_habitation,
    update_habitation,
    get_matches,
    get_all_matches,
    store_user_relation,
    get_user_relation,
    get_message_by_match
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
    UserAuth,
    MessageResponse
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
    allow_origins=["*"], # settings.allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

app.include_router(auth_router, prefix="/api")
app.include_router(chat_router, prefix="/api/chat", tags=["chat"])


@logs
@app.get("/api/get_regions", response_model=Dict[str, List[str]])
async def get_all_regions():
    regions = await get_regions()
    return {"regions": regions}
    

@logs
@app.get("/api/get_regions/{region_title}/cities", response_model=Dict[str, List[str]])
async def get_cities_by_region(region_title: str):
    cities = await get_cities_by_region_name(region_title)
    return {"localities": cities}


@logs
@app.get("/api/get_bad_habits", response_model=Dict[str, List[str]])
async def get_all_bad_habits():
    bad_habits = await get_bad_habits()
    return {"bad_habits": bad_habits}


@logs
@app.get("/api/get_interests", response_model=Dict[str, List[str]])
async def get_all_interests():
    interests = await get_interests()
    return {"interest": interests}


@logs
@app.get("/api/get_ed_dirs", response_model=Dict[str, List[Dict[str, str]]])
async def get_all_ed_dir():
    ed_dirs = await get_educ_dir()
    return {"ed_dirs":
            [
                {
                    "code": code,
                    "title": title
                }
                for code, title in ed_dirs
            ]
    }


@logs
@app.get("/api/get_messages", response_model=List[MessageResponse])
async def get_messages_endpoint(match_id: int):
    messages = await get_message_by_match(
        match_id
    )
    print(messages)
    return messages


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
