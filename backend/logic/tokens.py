from fastapi import Request, HTTPException, Depends
from typing import Annotated, Any

import jwt
import datetime
from passlib.context import CryptContext
from sqlalchemy.orm import Session

from .exceptions import AppError
from .users import UserRepository, UserService

from ..schemas.user import UserSchema, BaseModel
from ..models.user import User
from ..database import get_db
from ..utils.secret_data import TOKEN_ALGORITHM, SECRET_TOKEN_KEY
# from ..models.revoked_token import RevokedToken

class TokenResponse(BaseModel):
    access_token: str
    token_type: str

def get_user_repository(db: Session = Depends(get_db)) -> UserRepository:
    return UserRepository(db)

def get_user_service(repository: UserRepository = Depends(get_user_repository)) -> UserService:
    return UserService(repository)

ServiceDependency = Annotated[UserService, Depends(get_user_service)]

def generate_access_token(user_id: int, email: str) -> str:
    expires: datetime = datetime.datetime.now() + datetime.timedelta(minutes=1440)
    encode = {'sub': email, 'user_id': user_id, 'exp': expires}

    return jwt.encode(payload=encode, key=SECRET_TOKEN_KEY, algorithm=TOKEN_ALGORITHM)

async def get_current_user(request: Request,
                           service: ServiceDependency) -> UserSchema:
    cookie_token: str = request.cookies.get("token")
    payload_header: dict[str, Any] = jwt.decode(jwt=cookie_token, key=SECRET_TOKEN_KEY, algorithms=[TOKEN_ALGORITHM])
    user_id: int = payload_header['user_id']

    if user_id is None:
        raise HTTPException(status_code=401, detail="Invalid token.")
    
    try:
        return service.get_user(user_id)
    
    except AppError as e:
        raise HTTPException(status_code=e.error_code, detail=e.message)