from sqlalchemy.orm import Session, Query
from sqlalchemy.exc import NoResultFound, IntegrityError

from .exceptions import  ( 
    MemberNotFoundError, MemberAlreadyExistsError, 
    ChatNotFoundError, UserNotFoundError, AppError,
)
from ..schemas.member import ( 
    MemberCreateSchema, MemberSchema, 
    MembershipSchema, MemberUpdateSchema,
    MemberRole )
from ..schemas.chat import ChatSchema
from ..schemas.user import UserPublicSchema

from ..models.member import Member
from ..models.chat import Chat
from ..models.user import User

class MemberRepository:
    def __init__(self, db: Session):
        self.db = db

    def __to_member(self, data: MemberCreateSchema) -> Member:
        return Member(user_id=data.user_id, chat_id=data.chat_id, role=data.role)
    
    def __to_member_schema(self, member: Member):
        return MemberSchema(id=member.id, user_id=member.user_id, chat_id=member.chat_id, role=member.role)

    def add_member(self, create_schema: MemberCreateSchema) -> MemberSchema:
        member = self.__to_member(create_schema) 

        self.db.add(member)
        self.db.commit()

        return self.__to_member_schema(member)

    def find_member(self, id: int) -> MemberSchema:
        member = self.db.query(Member).filter(Member.id == id).first()

        if member is None:
            raise NoResultFound()
        
        return self.__to_member_schema(member)
    
    def find_member_by_user_and_chat(self, *, user_id: int, chat_id: int) -> MemberSchema:
        member = self.db.query(Member).filter(Member.user_id == user_id,
                                              Member.chat_id == chat_id).first()

        if member is None:
            raise NoResultFound()
        
        return self.__to_member_schema(member)
    
    def find_membership(self, user_id: int, chat_id: int) -> MemberSchema:
        membership = self.db.query(Member).filter(Member.user_id == user_id,
                                                  Member.chat_id == chat_id).first()
        
        if membership is None:
            raise NoResultFound()
        
        return self.__to_member_schema(membership)
    
    def find_chat_members(self, chat_id: int) -> list[UserPublicSchema]:
        users = self.db.query(User).join(Member).where(Member.chat_id == chat_id)

        if users is None or users.count() == 0:
            raise NoResultFound()
        
        return [UserPublicSchema(id=user.id, name=user.name, email=user.email,
                                 bio=user.bio, status=user.status, hashed_password=user.hashed_password,
                                 tag=user.tag) 
                                 for user in users]
    
    def update_member(self, user_id: int, chat_id: int, update_schema: MemberUpdateSchema) -> MemberSchema:
        member = self.db.query(Member).filter(Member.user_id == user_id,
                                              Member.chat_id == chat_id).first()
        if member is None:
            raise NoResultFound()
        
        if update_schema.role:
            member.role = update_schema.role

        return self.__to_member_schema(member)       
    
    def find_user_memberships(self, user_id: int) -> list[MemberSchema]:
        memberships = self.db.query(Member).filter(Member.user_id == user_id)

        if memberships is None or memberships.count() == 0:
            raise NoResultFound()

        return [self.__to_member_schema(membership)
                for membership in memberships]
    
    def delete_member(self, id: int) -> MemberSchema:
        member = self.db.query(Member).filter(Member.id == id).first()

        if member is None:
            raise NoResultFound()

        self.db.delete(member)
        self.db.commit()

        return self.__to_member_schema(member)
    
    def delete_membership(self, membership_schema: MembershipSchema) -> MemberSchema:
        membership = self.db.query(Member).filter(Member.user_id == membership_schema.user_id,
                                                  Member.chat_id == membership_schema.chat_id).first()

        if membership is None:
            raise NoResultFound()
        
        self.db.delete(membership)
        self.db.commit()

        return self.__to_member_schema(membership)
    

    # Current User
    def find_user_chats(self, user_id: int) -> list[ChatSchema]:
        result = self.db.query(Chat).join(Member).where(Member.user_id == user_id)
        chats = [ChatSchema(id=chat.id, name=chat.name, type=chat.type,
                            created_at=chat.created_at, updated_at=chat.updated_at)
                            for chat in result]
        
        if result is None or result.count() == 0:
            raise NoResultFound()
        
        return chats
    
    def is_user_in_chat(self, user_id: int, chat_id: int) -> bool:
        member = self.db.query(Member).filter(Member.user_id == user_id,
                                              Member.chat_id == chat_id).first()
        return member is not None
    
    def check_user_role(self, user_id: int, chat_id: int, role: MemberRole) -> bool:
        member = self.db.query(Member).filter(Member.user_id == user_id,
                                              Member.chat_id == chat_id).first()
        return member.role == role
