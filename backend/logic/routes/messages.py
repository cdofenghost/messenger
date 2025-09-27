from fastapi import APIRouter, Depends, HTTPException, Response
from typing import Annotated

from sqlalchemy.orm import Session

from ..tokens import get_current_user
from ..exceptions import AppError
from ..users import UserSchema
from ..messages import (
    MessageRepository, MessageService,
    MessageUpdateSchema, MessageCreateSchema, 
    MessageSchema,
)
from ..members import MemberRepository

from ...database import get_db

router = APIRouter()

def get_member_repository(db: Session = Depends(get_db)) -> MemberRepository:
    return MemberRepository(db)

def get_message_repository(db: Session = Depends(get_db)) -> MessageRepository:
    return MessageRepository(db)

def get_message_service(message_repository: MessageRepository = Depends(get_message_repository),
                        member_repository: MemberRepository = Depends(get_member_repository)) -> MessageService:
    return MessageService(message_repository=message_repository,
                          member_repository=member_repository)

MessageServiceDependency = Annotated[MessageService, Depends(get_message_service)]
UserDependency = Annotated[UserSchema, Depends(get_current_user)]
UpdateDependency = Annotated[MessageUpdateSchema, Depends()]

@router.post('/chats/{chat_id}/messages', response_model=MessageSchema, status_code=201, tags=["Message"])
async def send_message(chat_id: int,
                       user: UserDependency,
                       service: MessageServiceDependency,
                       create_data: MessageCreateSchema):
    try:
        return service.add_message(chat_id=chat_id, user_id=user.id, create_data=create_data)
    except AppError as e:
        raise HTTPException(status_code=e.error_code, detail=e.message)
    
@router.get('/chats/{chat_id}/messages', response_model=list[MessageSchema], status_code=200, tags=["Current User"])
async def get_chat_messages(chat_id: int,
                            user: UserDependency,
                            service: MessageServiceDependency,):
    try:
        return service.get_chat_messages(user_id=user.id, chat_id=chat_id)
    except AppError as e:
        raise HTTPException(status_code=e.error_code, detail=e.message)
    
# @router.get('/chats/{chat_id}/messages/search', response_model=list[MessageSchema], status_code=200, tags=["Message"])


@router.get('/chats/{chat_id}/messages/{id}', response_model=MessageSchema, status_code=200, tags=["Message"])
async def get_message(id: int,
                      service: MessageServiceDependency):
    try:
        return service.get_message(id=id)
    except AppError as e:
        raise HTTPException(status_code=e.error_code, detail=e.message)

    
@router.put('/chats/{chat_id}/messages/{id}', response_model=MessageSchema, status_code=200, tags=["Message"])
async def edit_message(chat_id: int, id: int,
                       user: UserDependency,
                       edit_data: MessageUpdateSchema,
                       service: MessageServiceDependency):
    try:
        return service.edit_message(id=id, chat_id=chat_id, user_id=user.id, edit_data=edit_data)
    except AppError as e:
        raise HTTPException(status_code=e.error_code, detail=e.message)

    
@router.delete('/chats/{chat_id}/messages/{id}', status_code=204, tags=["Message"])
async def delete_message(chat_id: int, id: int,
                         user: UserDependency,
                         service: MessageServiceDependency):
    try:
        service.delete_message(id=id, chat_id=chat_id, user_id=user.id)
    except AppError as e:
        raise HTTPException(status_code=e.error_code, detail=e.message)
