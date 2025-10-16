from typing import Optional, Literal
from pydantic import BaseModel, Field, field_validator
from datetime import datetime

from .message import MessageSchema

class ChatSchema(BaseModel):
    id: int = Field()
    name: str = Field()
    type: str = Field()
    created_at: datetime = Field()
    updated_at: datetime = Field()

class ChatPopupSchema(ChatSchema):
    last_message: Optional[MessageSchema] = None

Type = Literal["Direct Messages", "Private", "Public"]
class ChatCreateSchema(BaseModel):
    invited_user_ids: Optional[list[int]] = Field(default_factory=list)
    name: Optional[str] = None
    type: Type = "Private"

    # @field_validator('name')
    # def validate_name(cls, v, values):
    #     if values.get('type') != "Direct Messages" and not v:
    #         raise ValueError("Name is required for non-DM chats")
    #     return v

    # @field_validator('name')
    # def validate_dm_users(cls, v, values):
    #     if values.get('type') == "Direct Messages":
    #         if len(v) != 1:
    #             raise ValueError("DM chats must have exactly one invited user")
    #     return v

class ChatUpdateSchema(BaseModel):
    name: Optional[str] = None
    type: Optional[Type] = None

