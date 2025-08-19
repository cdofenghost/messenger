from fastapi import APIRouter, Depends, HTTPException, Response
from typing import Annotated

from sqlalchemy.orm import Session

from ..database import get_db
from .tokens import get_current_user, generate_access_token
from .exceptions import AppError
from .users import (
    UserRepository, UserService,
    UserCreateSchema, UserSchema, UserCredentialSchema,
)

router = APIRouter(tags=["User"])

def get_user_repository(db: Session = Depends(get_db)) -> UserRepository:
    return UserRepository(db)

def get_user_service(repository: UserRepository = Depends(get_user_repository)) -> UserService:
    return UserService(repository)

ServiceDependency = Annotated[UserService, Depends(get_user_service)]
UserDependency = Annotated[dict, Depends(get_current_user)]

@router.post("/register", response_model=UserSchema, status_code=201)
async def register(user_data: UserCreateSchema, 
                   service: ServiceDependency) -> UserSchema:

    try:
        user = service.register_user(user_data)
        return user
    
    except AppError as e:
        raise HTTPException(status_code=e.error_code, detail=e.message)


@router.post('/authorize')
async def authorize(credentials: UserCredentialSchema,
                    service: ServiceDependency,
                    response: Response):
    try:
        authorized_user: UserSchema = service.verify_credentials(credentials)
        token = generate_access_token(authorized_user.id, authorized_user.email)
        response.set_cookie("token", token)

        return {"access_token": token, "token_type": "bearer"}
    
    except AppError as e:
        raise HTTPException(status_code=e.error_code, detail=e.message)
        

# @router.get('/')
# async def get_user():


@router.delete('/', status_code=204)
async def remove_user(user_id: int,
                      service: ServiceDependency):
    try:
        service.remove_user(user_id)

    except AppError as e:
        raise HTTPException(status_code=e.error_code, detail=e.message)
    