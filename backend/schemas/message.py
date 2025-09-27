from typing import Optional

from pydantic import BaseModel, Field
from datetime import datetime

from .user import UserPublicSchema

class MessageSchema(BaseModel):
    id: int
    text: str
    sender: UserPublicSchema
    created_at: datetime
    updated_at: datetime

class MessageCreateSchema(BaseModel):
    text: str = Field()

class MessageUpdateSchema(BaseModel):
    text: str = Field()
