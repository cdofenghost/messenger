from fastapi import APIRouter, Depends, HTTPException, Response, Query
from typing import Annotated

from sqlalchemy.orm import Session

from ...database import get_db
from ..tokens import get_current_user, generate_access_token
from ..exceptions import AppError
from ..users import (
    UserRepository, UserService,
    UserCreateSchema, UserSchema, UserCredentialSchema,
    UserChangeDataSchema, UserPublicSchema,
)

router = APIRouter(prefix="/users")

def get_user_repository(db: Session = Depends(get_db)) -> UserRepository:
    return UserRepository(db)

def get_user_service(repository: UserRepository = Depends(get_user_repository)) -> UserService:
    return UserService(repository)

ServiceDependency = Annotated[UserService, Depends(get_user_service)]
UserDependency = Annotated[UserSchema, Depends(get_current_user)]
ChangeOptions = Annotated[UserChangeDataSchema, Depends()]

# Current User
@router.put('/me', tags=["Current User"], response_model=UserSchema, status_code=200)
async def change_current_user_data(change_data: ChangeOptions, 
                                   user: UserDependency,
                                   service: ServiceDependency,):
    try:
        return service.change_user_data(id=user.id, change_data=change_data)

    except AppError as e:
        raise HTTPException(status_code=e.error_code, detail=e.message)

@router.get('/me', tags=["Current User"], response_model=UserSchema, status_code=200)
async def get_current_user(user: UserDependency):
    try:
        return user

    except AppError as e:
        raise HTTPException(status_code=e.error_code, detail=e.message)

@router.delete('/me', tags=["Current User"], status_code=204)
async def remove_current_user(user: UserDependency,
                              service: ServiceDependency):
    try:
        service.remove_user(user.id)

    except AppError as e:
        raise HTTPException(status_code=e.error_code, detail=e.message)
    
# User
@router.post("/register", tags=["User"], response_model=UserSchema, status_code=201)
async def register(user_data: UserCreateSchema, 
                   service: ServiceDependency) -> UserSchema:
    try:
        user = service.register_user(user_data)
        return user
    
    except AppError as e:
        raise HTTPException(status_code=e.error_code, detail=e.message)


@router.post('/authorize', tags=["User"], response_model=dict[str, str], status_code=200)
async def authorize(credentials: UserCredentialSchema,
                    service: ServiceDependency,
                    response: Response):
    try:
        authorized_user: UserSchema = service.verify_credentials(credentials)
        token = generate_access_token(authorized_user.id, authorized_user.email)
        response.set_cookie("token", token, 
                            httponly=True,
                            samesite="lax",
                            max_age=30*24*3600,
                            secure=False)

        return {"access_token": token, "token_type": "bearer"}
    
    except AppError as e:
        raise HTTPException(status_code=e.error_code, detail=e.message)
    
@router.get('/search', tags=["User"], response_model=UserSchema | UserPublicSchema | list[UserPublicSchema], status_code=200)
async def search_user(service: ServiceDependency,
                      query: str = Query(..., min_length=1, description="Find user by e-mail, tag, or username")):
    try:
        found_user: UserSchema | UserPublicSchema = None

        if "@" in query and "." in query:
            found_user = service.get_user_by_email(email=query)
        elif query.startswith("@"):
            found_user = service.get_user_by_tag(tag=query)
        else:
            found_user = service.get_users_with_name(name=query)
        return found_user
    
    except AppError as e:
        raise HTTPException(status_code=e.error_code, detail=e.message)

    
@router.get('/{id}', tags=["User"], response_model=UserSchema, status_code=200)
async def get_user(id: int,
                   service: ServiceDependency):
    try:
        return service.get_user(id)

    except AppError as e:
        raise HTTPException(status_code=e.error_code, detail=e.message)
    

@router.get('/', tags=["User"], response_model=list[UserSchema], status_code=200)
async def get_all_users(service: ServiceDependency):
    return service.get_all_users()

@router.put('/{id}', tags=["User"], response_model=UserSchema, status_code=200)
async def change_user_data(id: int,
                           change_data: ChangeOptions, 
                           service: ServiceDependency,):
    try:
        return service.change_user_data(id=id, change_data=change_data)

    except AppError as e:
        raise HTTPException(status_code=e.error_code, detail=e.message)

@router.delete('/{id}', tags=["User"], status_code=204)
async def remove_user(user_id: int,
                      service: ServiceDependency):
    try:
        service.remove_user(user_id)

    except AppError as e:
        raise HTTPException(status_code=e.error_code, detail=e.message)
