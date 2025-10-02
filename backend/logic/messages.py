from sqlalchemy.orm import Session
from sqlalchemy.exc import NoResultFound

from .exceptions import (
    MessageNotFoundError,   
) 

from ..models.message import Message
from ..models.user import User
from ..models.member import Member
from ..schemas.message import (
    MessageSchema, MessageCreateSchema,
    MessageUpdateSchema,
)
from ..schemas.user import UserPublicSchema

from .members import MemberRepository, MemberNotFoundError

class MessageRepository:
    def __init__(self, db: Session):
        self.db = db

    def __to_message_schema(self, message: Message) -> MessageSchema:
        sender = self.db.query(User).join(Member).where(Member.id == message.sender_id).first()

        return MessageSchema(id=message.id, text=message.text, sender=UserPublicSchema.model_validate(sender), 
                             created_at=message.created_at, updated_at=message.edited_at)
    
    def __to_message(self, sender_id: int, create_schema: MessageCreateSchema) -> MessageSchema:
        message = Message(**create_schema.model_dump())
        message.sender_id = sender_id
        return message
    
    def add_message(self, sender_id: int, create_schema: MessageCreateSchema) -> MessageSchema:
        message = self.__to_message(sender_id=sender_id, create_schema=create_schema)

        if message is None:
            raise NoResultFound()
        
        self.db.add(message)
        self.db.commit()

        return self.__to_message_schema(message=message)
    
    def find_message(self, id: int) -> MessageSchema:
        message = self.db.query(Message).filter(Message.id == id).first()

        if message is None:
            raise NoResultFound()
        
        return self.__to_message_schema(message=message)

    def find_chat_messages(self, chat_id: int) -> MessageSchema:
        chat_messages = self.db.query(Message).join(Member).where(Member.chat_id == chat_id).order_by('created_at')

        if chat_messages is None or chat_messages.count() == 0:
            raise NoResultFound()
        
        return [self.__to_message_schema(message=message) 
                for message in chat_messages]
    
    def find_last_chat_message(self, chat_id: int) -> MessageSchema:
        message = self.db.query(Message).join(Member).where(Member.chat_id == chat_id).order_by(Message.created_at.desc()).first()

        if message is None:
            return None
        
        return self.__to_message_schema(message=message)

    def update_message(self, id: int, update_schema: MessageUpdateSchema) -> MessageSchema:
        message = self.db.query(Message).filter(Message.id == id).first()

        if message is None:
            raise NoResultFound()
        
        message.text = update_schema.text if update_schema.text else message.text
        self.db.merge(message)
        self.db.commit()

        return self.__to_message_schema(message=message)
    
    def delete_message(self, id: int) -> MessageSchema:
        message = self.db.query(Message).filter(Message.id == id).first()

        if message is None:
            raise NoResultFound()
        
        self.db.delete(message)
        self.db.commit()

        return self.__to_message_schema(message=message)
    
   
class MessageService:
    def __init__(self, message_repository: MessageRepository, member_repository: MemberRepository):
        self.repository = message_repository
        self.member_repository = member_repository
    
    def add_message(self, chat_id: int, user_id: int, create_data: MessageCreateSchema) -> MessageSchema:
        try:
            sender = self.member_repository.find_member_by_user_and_chat(chat_id=chat_id, user_id=user_id)
            return self.repository.add_message(sender_id=sender.id, create_schema=create_data)
        
        except NoResultFound:
            raise MemberNotFoundError()
    
    def get_message(self, id: int) -> MessageSchema:
        try:
            return self.repository.find_message(id=id)
        except NoResultFound:
            raise MessageNotFoundError()
        
    def get_chat_messages(self, chat_id: int, user_id: int) -> MessageSchema:
        try:
            if not self.member_repository.is_user_in_chat(user_id=user_id, chat_id=chat_id):
                raise MemberNotFoundError("You aren't participating in this chat.")
            return self.repository.find_chat_messages(chat_id=chat_id)
        
        except NoResultFound:
            raise MessageNotFoundError()
        
    def edit_message(self, id: int, chat_id: int, user_id: int, edit_data: MessageUpdateSchema) -> MessageSchema:
        try:
            if not self.member_repository.is_user_in_chat(user_id=user_id, chat_id=chat_id):
                raise MemberNotFoundError("You aren't participating in this chat.")
            return self.repository.update_message(id=id, update_schema=edit_data)
        
        except NoResultFound:
            raise MessageNotFoundError()

    def delete_message(self, id: int, chat_id: int, user_id: int) -> MessageSchema:
        try:
            if not self.member_repository.is_user_in_chat(user_id=user_id, chat_id=chat_id):
                raise MemberNotFoundError("You aren't participating in this chat.")
            return self.repository.delete_message(id=id)
        
        except NoResultFound:
            raise MessageNotFoundError()
