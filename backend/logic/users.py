from sqlalchemy.orm import Session
from sqlalchemy.exc import NoResultFound
from email_validator import validate_email

from passlib.hash import bcrypt

from ..utils.utils import generate_name
from ..models.user import User
from ..schemas.user import UserSchema, UserCreateSchema, UserCredentialSchema
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
        return User(
            name=generate_name(),
            email=credentials.email,
            hashed_password=hashed_password,
            bio="",
            status="",
        )
    
    def __to_user_schema(self, user: User) -> UserSchema:
        print(
            user.id, user.name, user.email,
            user.bio, user.status, user.hashed_password
        )
        return UserSchema(
            id=user.id, name=user.name, email=user.email,
            bio=user.bio, status=user.status, hashed_password=user.hashed_password
        )

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
    
    def remove_user(self, id: int) -> UserSchema:
        user = self.db.query(User).filter(User.id == id).first()

        if user is None:
            raise NoResultFound()
        
        self.db.delete(user)

        return self.__to_user_schema(user)


class UserService:
    def __init__(self, repository: UserRepository):
        self.repository = repository

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
    
    def remove_user(self, id: int) -> UserSchema:
        try:
            deleted_user: UserSchema = self.repository.remove_user(id)
            return deleted_user
        
        except NoResultFound:
            raise UserNotFoundError()
        

    def verify_credentials(self, credentials: UserCredentialSchema) -> UserSchema:
        user: UserSchema = self.get_user_by_email(credentials.email)

        if not bcrypt.verify(credentials.password, user.hashed_password):
            raise InvalidCredentialsError()
        
        return user