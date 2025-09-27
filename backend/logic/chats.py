from sqlalchemy.orm import Session
from sqlalchemy.exc import NoResultFound

from .exceptions import  (
    ChatNotFoundError, MemberRoleError,
    MemberNotFoundError,
)
from .members import MemberRepository

from ..models.chat import Chat
from ..schemas.chat import ( 
    ChatSchema, ChatCreateSchema,
    ChatUpdateSchema,
)
from ..schemas.user import (
    UserPublicSchema
)
from ..schemas.member import (
    MemberRole, ADMIN, PARTICIPANT,
    MemberSchema, MemberCreateSchema,
)

class ChatRepository:
    def __init__(self, db: Session):
        self.db = db

    def __to_chat(self, chat_schema: ChatCreateSchema) -> Chat:
        return Chat(name=chat_schema.name, type=chat_schema.type)
    
    def __to_chat_schema(self, chat: Chat) -> ChatSchema:
        return ChatSchema(id=chat.id, name=chat.name, 
                          type=chat.type, created_at=chat.created_at,
                          updated_at=chat.updated_at)
    
    def add_chat(self, create_schema: ChatCreateSchema) -> ChatSchema:
        chat = self.__to_chat(create_schema)
        
        self.db.add(chat)
        self.db.commit()

        return self.__to_chat_schema(chat)
    
    def find_chat(self, id: int) -> ChatSchema:
        chat = self.db.query(Chat).filter(Chat.id == id).first()

        if chat is None:
            raise NoResultFound()
        
        return self.__to_chat_schema(chat)
    
    def find_chats_by_name(self, name: str) -> list[ChatSchema]:
        chats = self.db.query(Chat).filter(Chat.name == name)

        if chats is [] or chats is None:
            raise NoResultFound()

        return [self.__to_chat_schema(chat) for chat in chats]
    
    def update_chat(self, id: int, update_schema: ChatUpdateSchema) -> ChatSchema:
        chat = self.db.query(Chat).filter(Chat.id == id).first()

        if chat is None:
            raise NoResultFound()

        chat.name = update_schema.name if update_schema.name else chat.name
        chat.type = update_schema.type if update_schema.type else chat.type

        self.db.merge(chat)
        self.db.commit()

        return self.__to_chat_schema(chat)
    
    def delete_chat(self, id: int) -> ChatSchema:
        chat = self.db.query(Chat).filter(Chat.id == id).first()

        if chat is None:
            raise NoResultFound()   

        self.db.delete(chat)
        self.db.commit()

        return self.__to_chat_schema(chat)
    

class ChatService:
    def __init__(self, chat_repository: ChatRepository, member_repository: MemberRepository):
        self.repository = chat_repository
        self.member_repository = member_repository

    def add_chat(self, chat_data: ChatCreateSchema) -> ChatSchema:
        chat_data.name = chat_data.name if chat_data.name else "Chat Name"
        return self.repository.add_chat(chat_data)

    def get_chat(self, id: int) -> ChatSchema:
        try:
            return self.repository.find_chat(id)
        
        except NoResultFound:
            raise ChatNotFoundError()
    
    def get_chats_by_name(self, name: str) -> list[ChatSchema]:
        try:
            return self.repository.find_chats_by_name(name)
        
        except NoResultFound:
            raise ChatNotFoundError(message=f"No chats under the name '{name}'.")
    
    def update_chat(self, id: int, chat_data: ChatUpdateSchema) -> ChatSchema:
        try:
            return self.repository.update_chat(id, chat_data)
        
        except NoResultFound:
            raise ChatNotFoundError()
        
    def delete_chat(self, id: int) -> ChatSchema:
        try:
            return self.repository.delete_chat(id)
        
        except NoResultFound:
            raise ChatNotFoundError()

    def remove_user_from_chat(self, user_id: int, user_remove_id: int, chat_id: int) -> UserPublicSchema:
        is_user_admin = self.member_repository.check_user_role(user_id=user_id, chat_id=chat_id, role=ADMIN)
        if not is_user_admin:
            raise MemberRoleError("Only chat administrator can perform this aciton.")
        
        try:
            user_to_remove = self.member_repository.find_member_by_user_and_chat(user_id=user_remove_id, chat_id=chat_id)
            self.member_repository.delete_member(user_to_remove.id)

        except NoResultFound:
            raise MemberNotFoundError()

    def get_chat_members(self, chat_id: int) -> list[UserPublicSchema]:
        try:
            return self.member_repository.find_chat_members(chat_id=chat_id)
        except NoResultFound:
            raise MemberNotFoundError()
        
    def get_user_chats(self, user_id: int) -> list[ChatSchema]:
        try:
            return self.member_repository.find_user_chats(user_id=user_id)
        except NoResultFound:
            raise MemberNotFoundError()
        
    def add_member_to_chat(self, create_schema: MemberCreateSchema) -> MemberSchema:
        try:
            return self.member_repository.add_member(create_schema=create_schema)
        except NoResultFound:
            raise MemberNotFoundError()
