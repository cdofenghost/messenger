from fastapi import APIRouter, Depends, HTTPException, Query
from typing import Annotated, Optional

from sqlalchemy.orm import Session

from ..tokens import get_current_user
from ..exceptions import AppError
from ..chats import ( 
    ChatRepository, ChatService,
    ChatCreateSchema, ChatSchema,
    ChatUpdateSchema,
)
from ..members import (
    MemberRepository,
    MemberCreateSchema, MemberSchema,
    MembershipSchema, MemberUpdateSchema
)

from ...database import get_db
from ...schemas.user import UserPublicSchema, UserSchema
router = APIRouter()

ADMIN = "Admin"
PARTICIPANT = "Participant"

def get_chat_repository(db: Session = Depends(get_db)) -> ChatRepository:
    return ChatRepository(db)

def get_member_repository(db: Session = Depends(get_db)) -> MemberRepository:
    return MemberRepository(db)

def get_chat_service(chat_repository: ChatRepository = Depends(get_chat_repository),
                     member_repository: ChatRepository = Depends(get_member_repository)) -> ChatService:
    return ChatService(chat_repository=chat_repository, member_repository=member_repository)

ChatServiceDependency = Annotated[ChatService, Depends(get_chat_service)]
UserDependency = Annotated[UserSchema, Depends(get_current_user)]

UpdateSchema = Annotated[ChatUpdateSchema, Depends()]

@router.get('/chats/{id}', response_model=ChatSchema, status_code=200, tags=["Chat"])
async def get_chat(id: int,
                   service: ChatServiceDependency) -> ChatSchema:
    try:
        return service.get_chat(id)
    except AppError as e:
        raise HTTPException(status_code=e.error_code, detail=e.message)

@router.put('/chats/{id}', response_model=ChatSchema, status_code=200, tags=["Chat"])
async def update_chat(id: int, 
                      service: ChatServiceDependency,
                      chat_data: UpdateSchema) -> ChatSchema:
    try:
        return service.update_chat(id, chat_data)
    except AppError as e:
        raise HTTPException(status_code=e.error_code, detail=e.message)
    
@router.delete('/chats/{id}', status_code=204, tags=["Chat"])
async def delete_chat(id: int,
                      service: ChatServiceDependency):
    try:
        service.delete_chat(id)
    except AppError as e:
        raise HTTPException(status_code=e.error_code, detail=e.message) 

@router.get('/chats/{chat_id}/members', response_model=list[UserPublicSchema], tags=["Chat"])
async def get_chat_members(chat_id: int,
                           service: ChatServiceDependency):
    try:
        return service.get_chat_members(chat_id)
    except AppError as e:
        raise HTTPException(status_code=e.error_code, detail=e.message)
    
@router.delete('/chats/{chat_id}/members/{user_id}', status_code=204, tags=["Chat"])
async def remove_chat_member(chat_id: int, user_id: int,
                             user: UserDependency,
                             service: ChatServiceDependency):
    try:
        service.remove_user_from_chat(user_id=user.id, user_remove_id=user_id, chat_id=chat_id)
    except AppError as e:
        raise HTTPException(status_code=e.error_code, detail=e.message)
    
@router.put('/chats/{chat_id}/members/{user_id}', response_model=MemberSchema,  status_code=201, tags=["Chat"])
async def change_member_role(chat_id: int, user_id: int,
                             user: UserDependency,
                             service: ChatServiceDependency,
                             update_schema: MemberUpdateSchema = Depends(),):
    try:
        return service.change_member_role(chat_id=chat_id, user_id=user.id,
                                          user_update_id=user_id,
                                          update_schema=update_schema)
    except AppError as e:
        raise HTTPException(status_code=e.error_code, detail=e.message)
    
@router.get('/chats/{chat_id}/members/{user_id}', response_model=MemberSchema, status_code=200, tags=["Chat"])
async def get_member_info(chat_id: int, user_id: int,
                          user: UserDependency,
                          service: ChatServiceDependency):
    try:
        return service.get_member(chat_id=chat_id, user_id=user_id)
    except AppError as e:
        raise HTTPException(status_code=e.error_code, detail=e.message)
    
# Current User
@router.get('/users/me/chats', status_code=200, tags=["Current User"], response_model=list[ChatSchema])
async def get_user_chats(user: UserDependency,
                         service: ChatServiceDependency):
    try:
        return service.get_user_chats(user.id)
    except AppError as e:
        raise HTTPException(status_code=e.error_code, detail=e.message)

@router.post('/users/me/chats', response_model=ChatSchema, status_code=201, tags=["Current User"])
async def create_chat(invited_user_id: int,
                      user: UserDependency, 
                      service: ChatServiceDependency,
                      chat_data: ChatCreateSchema = Depends()) -> ChatSchema:
    chat = service.add_chat(chat_data)

    service.add_member_to_chat(MemberCreateSchema(user_id=user.id, chat_id=chat.id, role=ADMIN))
    service.add_member_to_chat(MemberCreateSchema(user_id=invited_user_id, chat_id=chat.id, role=PARTICIPANT))

    return chat

@router.post('/chats/{chat_id}/members', tags=["Chat"])
async def add_user_to_public_chat(chat_id: int,
                                  invited_user_id: int,
                                  service: ChatServiceDependency) -> MemberSchema:
    try:
        member = MemberCreateSchema(user_id=invited_user_id, chat_id=chat_id, role=PARTICIPANT)
        return service.add_member_to_chat(member)

    except AppError as e:
        raise HTTPException(status_code=e.error_code, detail=e.message)
