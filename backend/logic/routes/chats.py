from fastapi import APIRouter, Depends, HTTPException
from typing import Annotated, Optional

from sqlalchemy.orm import Session

from ..tokens import get_current_user
from ..exceptions import AppError
from ..chats import ( 
    ChatRepository, ChatService,
    ChatCreateSchema, ChatSchema,
    ChatUpdateSchema, CreatePublicChatSchema,
    CreatePrivateChatSchema,
)
from ..particpants import (
    ParticipantRepository, ParticipantService,
    ParticipantCreateSchema, ParticipantSchema,
    ParticipationSchema, 
)

from ...database import get_db
from ...schemas.user import UserSchema
router = APIRouter(tags=["Chat"], prefix="/chats")

def get_chat_repository(db: Session = Depends(get_db)) -> ChatRepository:
    return ChatRepository(db)

def get_chat_service(repository: ChatRepository = Depends(get_chat_repository)) -> ChatService:
    return ChatService(repository)

def get_participant_repository(db: Session = Depends(get_db)) -> ParticipantRepository:
    return ParticipantRepository(db)

def get_participant_service(repository: ChatRepository = Depends(get_participant_repository)) -> ParticipantService:
    return ParticipantService(repository)

ChatServiceDependency = Annotated[ChatService, Depends(get_chat_service)]
ParticipantServiceDependency = Annotated[ParticipantService, Depends(get_participant_service)]
UserDependency = Annotated[UserSchema, Depends(get_current_user)]

UpdateSchema = Annotated[ChatUpdateSchema, Depends()]

@router.post('/private', response_model=ChatSchema, status_code=201)
async def create_private_chat(chat_data: CreatePrivateChatSchema,
                              invited_user_id: int,
                              user: UserDependency, 
                              participant_service: ParticipantServiceDependency,
                              chat_service: ChatServiceDependency) -> ChatSchema:
    chat = chat_service.add_chat(chat_data)

    participant_service.add_participant(ParticipantCreateSchema(user_id=user.id, chat_id=chat.id))
    participant_service.add_participant(ParticipantCreateSchema(user_id=invited_user_id, chat_id=chat.id))

    return chat


@router.post('/public', response_model=ChatSchema, status_code=201)
async def create_public_chat(chat_data: CreatePublicChatSchema,
                             user: UserDependency,
                             participant_service: ParticipantServiceDependency,
                             chat_service: ChatServiceDependency,
                             invited_user_id: Optional[int] = None) -> ChatSchema:
    chat = chat_service.add_chat(chat_data)

    participant_service.add_participant(ParticipantCreateSchema(user_id=user.id, chat_id=chat.id))
    if invited_user_id:
        participant_service.add_participant(ParticipantCreateSchema(user_id=user.id, chat_id=chat.id))

    return chat


@router.post('/public/add')
async def add_user_to_public_chat(participant_schema: ParticipantCreateSchema,
                                  user: UserDependency,
                                  chat_service: ChatServiceDependency,
                                  participant_service: ParticipantServiceDependency) -> ParticipantSchema:
    try:
        chat_service.get_chat(participant_schema.chat_id)
        return participant_service.add_participant(user_id=participant_schema.user_id, chat_id=participant_schema.chat_id)

    except AppError as e:
        raise HTTPException(status_code=e.error_code, detail=e.message)
    
@router.get('/{id}', response_model=ChatSchema, status_code=200)
async def get_chat(id: int,
                   service: ChatServiceDependency) -> ChatSchema:
    try:
        return service.get_chat(id)
    except AppError as e:
        raise HTTPException(status_code=e.error_code, detail=e.message)

@router.put('/', response_model=ChatSchema, status_code=200)
async def update_chat(id: int, chat_data: UpdateSchema,
                      service: ChatServiceDependency) -> ChatSchema:
    try:
        return service.update_chat(id, chat_data)
    except AppError as e:
        raise HTTPException(status_code=e.error_code, detail=e.message)
    
@router.delete('/', status_code=204)
async def delete_chat(id: int,
                      service: ChatServiceDependency):
    try:
        service.delete_chat(id)
    except AppError as e:
        raise HTTPException(status_code=e.error_code, detail=e.message) 
    

@router.get('/{id}/participants', response_model=list[ParticipantSchema])
async def get_chat_participants(chat_id: int,
                                service: ParticipantServiceDependency):
    try:
        return service.get_chat_participants(chat_id)
    except AppError as e:
        raise HTTPException(status_code=e.error_code, detail=e.message)
    
@router.get('/participant/{id}', response_model=ParticipantSchema, status_code=200)
async def get_chat_participant(id: int,
                                      service: ParticipantServiceDependency):
    try:
        return service.get_participant(id)
    except AppError as e:
        raise HTTPException(status_code=e.error_code, detail=e.message)
    
@router.delete('/participant', status_code=204)
async def remove_chat_participant(id: int,
                                         service: ParticipantServiceDependency):
    try:
        service.remove_participant(id)
    except AppError as e:
        raise HTTPException(status_code=e.error_code, detail=e.message)


@router.get('/participations', response_model=list[ParticipantSchema])
async def get_user_participations(user_id: int,
                                  service: ParticipantServiceDependency):
    try:
        return service.get_user_participations(user_id)
    except AppError as e:
        raise HTTPException(status_code=e.error_code, detail=e.message)
    
@router.get('/participation', response_model=ParticipantSchema, status_code=200)
async def get_user_participations(user_id: int,
                                  service: ParticipantServiceDependency):
    try:
        return service.get_participation(user_id)
    except AppError as e:
        raise HTTPException(status_code=e.error_code, detail=e.message)

@router.delete('/participation', status_code=204)
async def remove_chat_participation(participation: ParticipationSchema,
                                           service: ParticipantServiceDependency):
    try:
        service.remove_participation(participation)
    except AppError as e:
        raise HTTPException(status_code=e.error_code, detail=e.message)