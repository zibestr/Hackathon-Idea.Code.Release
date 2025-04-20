from time import time
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from passlib.context import CryptContext
from typing import Optional, Dict, Tuple, Annotated

from config import settings
from utils import logs
from db import (
    get_user_by_email,
    create_user,
    get_matches,
    get_all_matches
)

from utils import (
    ModelReadiness,
    TextRequest,
    RankingPairRequest,
    NSFWRequest,
    Token,
    TokenData,
    UserData,
    UserIdentify,
    UserAuth
)

router = APIRouter(prefix="/auth", tags=["auth"])
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token")


@logs
def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


@logs
def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


@logs
async def authenticate_user(email: str, password: str) -> Optional[UserAuth]:
    user = await get_user_by_email(email)
    if not user or not verify_password(password, user.hashed_password):
        return None
    return user


@logs
def create_access_token(data: dict) -> str:
    to_encode = data.copy()
    expire = time() + settings.access_token_expire_seconds
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, settings.secret_key, algorithm=settings.encryption_algorithm)


@logs
async def get_current_user(token: str = Depends(oauth2_scheme)) -> UserData:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, settings.secret_key, algorithms=[settings.encryption_algorithm])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
        token_data = TokenData(email=email)
    except JWTError:
        raise credentials_exception
    
    user = await get_user_by_email(token_data.email)
    if user is None:
        raise credentials_exception
    return user


@logs
async def get_current_active_user(current_user: UserData = Depends(get_current_user)) -> UserData:
    if not get_user_by_email(current_user.email).is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user


@logs
@router.post("/token", response_model=Token)
async def login_for_access_token(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    user = await authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = create_access_token(data={"sub": user.email})
    return {"access_token": access_token, "token_type": "bearer"}


@logs
@router.post("/register", response_model=Token, status_code=status.HTTP_201_CREATED)
async def register_user(user_data: UserAuth):
    existing_user = await get_user_by_email(user_data.email)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    user_data.hashed_password = get_password_hash(user_data.hashed_password)
    new_user = await create_user(user_data)
    if new_user is None:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=f"Users profile bio too toxic."
        )
    
    access_token = create_access_token(data={"sub": new_user.email})
    return {"access_token": access_token, "token_type": "bearer"}


@logs
@router.post("/login", response_model=Token)
async def login(form_data: UserIdentify):
    user = await authenticate_user(form_data.email, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token = create_access_token(data={"sub": user.email})
    return {"access_token": access_token, "token_type": "bearer"}


@logs
@router.get("/me", response_model=UserData)
async def read_users_me(current_user: UserData = Depends(get_current_active_user)):
    return current_user
