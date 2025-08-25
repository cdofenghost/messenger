from sqlalchemy.orm import Session
from sqlalchemy.exc import NoResultFound

from .exceptions import  (
    ChatNotFoundError,
)

from ..models.chat import Chat
from ..schemas.chat import ( 
    ChatSchema, ChatCreateSchema,
    ChatUpdateSchema, CreatePublicChatSchema,
    CreatePrivateChatSchema
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
    def __init__(self, repository: ChatRepository):
        self.repository = repository

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
        
    def delete_chat(self, id: int):
        try:
            return self.repository.delete_chat(id)
        
        except NoResultFound:
            raise ChatNotFoundError()