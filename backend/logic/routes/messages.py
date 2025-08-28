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

from ...database import get_db

router = APIRouter(tags=["Message"], prefix="/messages")

def get_message_repository(db: Session = Depends(get_db)) -> MessageRepository:
    return MessageRepository(db)

def get_message_service(repository: MessageRepository = Depends(get_message_repository)) -> MessageService:
    return MessageService(repository)

ServiceDependency = Annotated[MessageService, Depends(get_message_service)]
UserDependency = Annotated[UserSchema, Depends(get_current_user)]
UpdateDependency = Annotated[MessageUpdateSchema, Depends()]

@router.post('/', response_model=MessageSchema, status_code=201)
def send_message(message_data: MessageCreateSchema,
                 service: ServiceDependency):
    try:
        return service.add_message(message_data)
    except AppError as e:
        raise HTTPException(status_code=e.error_code, detail=e.message)
    
@router.get('/{id}', response_model=MessageSchema, status_code=200)
def get_message(id: int,
                service: ServiceDependency):
    try:
        return service.get_message(id)
    except AppError as e:
        raise HTTPException(status_code=e.error_code, detail=e.message)
    
@router.get('/', response_model=MessageSchema, status_code=200)
def get_message_by_text(text: str,
                        service: ServiceDependency):
    try:
        return service.get_message_by_text(text)
    except AppError as e:
        raise HTTPException(status_code=e.error_code, detail=e.message)

@router.get('/', response_model=list[MessageSchema], status_code=200)
def get_messages_by_text(text: str,
                        service: ServiceDependency):
    try:
        return service.get_messages_by_text(text)
    except AppError as e:
        raise HTTPException(status_code=e.error_code, detail=e.message)
    
@router.put('/', response_model=MessageSchema, status_code=200)
def edit_message(id: int,
                 message_data: MessageUpdateSchema,
                 service: ServiceDependency):
    try:
        return service.edit_message(id, message_data)
    except AppError as e:
        raise HTTPException(status_code=e.error_code, detail=e.message)
    
@router.delete('/', status_code=204)
def remove_message(id: int,
                   service: ServiceDependency):
    try:
        service.remove_message(id)
    except AppError as e:
        raise HTTPException(status_code=e.error_code, detail=e.message)