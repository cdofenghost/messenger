from sqlalchemy.orm import Session
from sqlalchemy.exc import NoResultFound
from email_validator import validate_email, EmailNotValidError, EmailUndeliverableError

from passlib.hash import bcrypt

from ..utils.utils import generate_name, generate_user_tag
from ..models.user import User
from ..schemas.user import ( 
    UserSchema, UserCreateSchema, 
    UserCredentialSchema, UserChangeDataSchema,
    UserPublicSchema
)
from .exceptions import (
    InvalidCredentialsError, 
    InvalidEmailError,
    UserNotFoundError,
    UserAlreadyRegisteredError
)

class UserRepository:
    def __init__(self, db: Session):
        self.db = db

    def __to_user(self, credentials: UserCreateSchema) -> User:
        hashed_password = bcrypt.hash(credentials.password)
        user_tag = None
        while user_tag is None or self.__is_user_tag_taken(tag=user_tag):
            user_tag = generate_user_tag()
        return User(
            name=generate_name(),
            tag=user_tag,
            email=credentials.email,
            hashed_password=hashed_password,
            bio="",
            status="",
        )
    
    def __to_user_schema(self, user: User) -> UserSchema:
        return UserSchema(
            id=user.id, name=user.name, email=user.email,
            bio=user.bio, status=user.status, hashed_password=user.hashed_password,
            tag=user.tag
        )
    
    def __is_user_tag_taken(self, tag: str) -> bool:
        return self.db.query(User).filter(User.tag == tag).first() != None

    def add_user(self, credentials: UserCreateSchema) -> UserSchema:
        user = self.__to_user(credentials)

        self.db.add(user)
        self.db.commit()

        return self.__to_user_schema(user)
    
    def find_user(self, id: int) -> UserSchema:
        user = self.db.query(User).filter(User.id == id).first()

        if user is None:
            raise NoResultFound()
        
        return self.__to_user_schema(user)
    
    def find_user_by_email(self, email: str) -> UserSchema:
        user = self.db.query(User).filter(User.email == email).first()

        if user is None:
            raise NoResultFound()
        
        return self.__to_user_schema(user)
    
    def find_user_by_tag(self, tag: str) -> UserSchema:
        user = self.db.query(User).filter(User.tag == tag).first()

        if user is None:
            raise NoResultFound()
        
        return self.__to_user_schema(user=user)
    
    def find_users_with_name(self, name: str) -> list[UserSchema]:
        users = self.db.query(User).filter(User.name.like(f"%{name}%"))

        if users is None or users.count() == 0:
            raise NoResultFound()
        
        return [self.__to_user_schema(user=user)
                for user in users]
    
    def get_all_users(self) -> list[UserSchema]:
        users = self.db.query(User).all()
        return [self.__to_user_schema(user) for user in users]
    
    def change_user_data(self, id: int, changed_data: UserChangeDataSchema) -> UserSchema:
        user = self.db.query(User).filter(User.id == id).first()

        if user is None:
            raise NoResultFound()

        user.name = changed_data.name if changed_data.name else user.name
        user.email = changed_data.email if changed_data.email else user.email
        user.bio = changed_data.bio if changed_data.bio else user.bio
        user.hashed_password = bcrypt.hash(changed_data.password) if changed_data.password else user.hashed_password
        
        self.db.merge(user)
        self.db.commit()

        return self.__to_user_schema(user)

    def remove_user(self, id: int) -> UserSchema:
        user = self.db.query(User).filter(User.id == id).first()

        if user is None:
            raise NoResultFound()
        
        self.db.delete(user)
        self.db.commit()

        return self.__to_user_schema(user)


class UserService:
    def __init__(self, repository: UserRepository):
        self.repository = repository

    def __to_public_schema(self, user: UserSchema) -> UserPublicSchema:
        return UserPublicSchema(id=user.id, name=user.name, tag=user.tag,
                                bio=user.bio, status=user.status)

    def register_user(self, credentials: UserCreateSchema) -> UserSchema:
        try:
            self.get_user_by_email(credentials.email)
            raise UserAlreadyRegisteredError()

        except UserNotFoundError:
            try:
                validate_email(credentials.email)
            except:
                raise InvalidEmailError()

            if credentials.password != credentials.repeated_password:
                raise InvalidCredentialsError("Password doesn't match the repeated password. Try again.")

            return self.repository.add_user(credentials)
    
    def get_user(self, id: int) -> UserSchema:
        try:
            found_user: UserSchema = self.repository.find_user(id)
            return found_user

        except NoResultFound:
            raise UserNotFoundError()
    
    def get_user_by_email(self, email: str) -> UserSchema:
        try:
            found_user: UserSchema = self.repository.find_user_by_email(email)
            return found_user
        
        except NoResultFound:
            raise UserNotFoundError()
        
    def get_user_by_tag(self, tag: str) -> UserPublicSchema:
        try:
            found_user: UserSchema = self.repository.find_user_by_tag(tag=tag)
            return self.__to_public_schema(user=found_user)
        
        except NoResultFound:
            raise UserNotFoundError("No user found with such tag.")
        
    def get_users_with_name(self, name: str) -> list[UserPublicSchema]:
        try:
            found_users: list[UserSchema] = self.repository.find_users_with_name(name=name)
            return [self.__to_public_schema(user=user)
                    for user in found_users]

        except NoResultFound:
            raise UserNotFoundError("No user found with such nickname.")
        
    def get_all_users(self) -> list[UserSchema]:
        return self.repository.get_all_users()
        
    def change_user_data(self, id: int, change_data: UserChangeDataSchema) -> UserSchema:
        if change_data.email:
            self.is_email_valid(change_data.email)

        try:
            return self.repository.change_user_data(id=id, changed_data=change_data)

        except NoResultFound:
            raise UserNotFoundError()

    def remove_user(self, id: int) -> UserSchema:
        try:
            deleted_user: UserSchema = self.repository.remove_user(id)
            return deleted_user
        
        except NoResultFound:
            raise UserNotFoundError()
        
    def is_already_registered(self, email: str):
        try:
            self.get_user_by_email(email=email)
            raise UserAlreadyRegisteredError()
        except:
            return True
    
    def is_email_valid(self, email: str):
        try:
            validate_email(email, check_deliverability=True)
            return True
        
        except (EmailUndeliverableError, EmailNotValidError):
            raise InvalidEmailError()
        

    def verify_credentials(self, credentials: UserCredentialSchema) -> UserSchema:
        user: UserSchema = self.get_user_by_email(credentials.email)

        if not bcrypt.verify(credentials.password, user.hashed_password):
            raise InvalidCredentialsError()
        
        return user
