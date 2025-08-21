from typing import Optional
from pydantic import BaseModel, EmailStr, Field, constr

class UserSchema(BaseModel):
    id: int = Field()
    name: str = Field(pattern="[А-Яа-яA-Za-z0-9]+", min_length=2, max_length=50)
    email: EmailStr = Field()
    bio: str = Field(max_length=250)
    status: str = Field()
    hashed_password: str = Field()

class UserCredentialSchema(BaseModel):
    email: EmailStr = Field()
    password: str = Field(pattern="^[a-zA-Z0-9!#$%&*+.<=>?@^_]+$", min_length=8, max_length=16)

class UserCreateSchema(UserCredentialSchema):
    repeated_password: str = Field(pattern="^[a-zA-Z0-9!#$%&*+.<=>?@^_]+$", min_length=8, max_length=16)

class SetUsernameRequest(BaseModel):
    name: str = Field(pattern="[А-Яа-яA-Za-z0-9]+", min_length=2, max_length=50)

class UserChangeDataSchema(BaseModel):
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    bio: Optional[str] = None
    password: Optional[str] = None