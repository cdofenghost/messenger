from sqlalchemy.orm import Session
from sqlalchemy.exc import NoResultFound

from .exceptions import (
    MessageNotFoundError,   
) 

from ..models.message import Message
from ..schemas.message import (
    MessageSchema, MessageCreateSchema,
    MessageUpdateSchema,
)

class MessageRepository:
    def __init__(self, db: Session):
        self.db = db

    def __to_message(self, create_schema: MessageCreateSchema) -> Message:
        return Message(**create_schema.model_dump())
    
    def __to_message_schema(self, message: Message) -> MessageSchema:
        return MessageSchema(id=message.id, sender_id=message.sender_id, text=message.text)
    
    def add_message(self, create_schema: MessageCreateSchema) -> MessageSchema:
        message = self.__to_message(create_schema)

        self.db.add(message)
        self.db.commit()

        return self.__to_message_schema(message)
    
    def find_message(self, id: int) -> MessageSchema:
        message = self.db.query(Message).filter(Message.id == id).first()

        if message is None:
            raise NoResultFound()
        
        return self.__to_message_schema(message)
    
    def find_message_by_text(self, text: str) -> MessageSchema:
        message = self.db.query(Message).filter(Message.text.contains(text)).first()

        if message is None:
            raise NoResultFound()
        
        return self.__to_message_schema(message)

    def find_messages_by_text(self, text: str) -> list[MessageSchema]:
        messages = self.db.query(Message).filter(text in Message.text)

        if messages.count() == 0 or messages is None:
            raise NoResultFound()
        
        return [self.__to_message_schema(message)
                for message in messages]
    
    def update_message(self, id: int, update_schema: MessageUpdateSchema) -> MessageSchema:
        message = self.db.query(Message).filter(Message.id == id).first()

        if message is None:
            raise NoResultFound()
        
        message.text = update_schema.text if update_schema.text else message.text

        self.db.merge(message)
        self.db.commit()

        return self.__to_message_schema(message)
    

    def delete_message(self, id: int) -> MessageSchema:
        message = self.db.query(Message).filter(Message.id == id).first()

        if message is None:
            raise NoResultFound()
        
        self.db.delete(message)
        self.db.commit()

        return self.__to_message_schema(message)
    

class MessageService:
    def __init__(self, repository: MessageRepository):
        self.repository = repository

    def add_message(self, message_data: MessageCreateSchema) -> MessageSchema:
        return self.repository.add_message(message_data)
    
    def get_message(self, id: int) -> MessageSchema:
        try:
            return self.repository.find_message(id)
        except:
            raise MessageNotFoundError()
        
    def get_message_by_text(self, text: str) -> MessageSchema:
        try:
            return self.repository.find_message_by_text(text)
        except:
            raise MessageNotFoundError()
        
    def get_messages_by_text(self, text: str) -> list[MessageSchema]:
        try:
            return self.repository.find_messages_by_text(text)
        except:
            raise MessageNotFoundError()
        
    def edit_message(self, id: int, edit_data: MessageUpdateSchema) -> MessageSchema:
        try:
            return self.repository.update_message(id, edit_data)
        except:
            raise MessageNotFoundError()
        
    def remove_message(self, id: int) -> MessageSchema:
        try:
            return self.repository.delete_message(id)
        except:
            raise MessageNotFoundError()
        
        
        
