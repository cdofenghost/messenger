from typing import Optional

from pydantic import BaseModel, Field
from datetime import datetime

class ChatSchema(BaseModel):
    id: int = Field()
    name: str = Field()
    type: str = Field()
    created_at: datetime = Field()
    updated_at: datetime = Field()


class ChatCreateSchema(BaseModel):
    name: Optional[str] = None
    type: Optional[str] = None

class CreatePrivateChatSchema(ChatCreateSchema):
    type: str = "Private"

class CreatePublicChatSchema(ChatCreateSchema):
    type: str = "Public"

class ChatUpdateSchema(BaseModel):
    name: Optional[str] = None
    type: Optional[str] = None

