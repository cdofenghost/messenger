from typing import Optional

from pydantic import BaseModel, Field
from datetime import datetime

class MessageSchema(BaseModel):
    id: int = Field()
    sender_id: int = Field()
    text: str = Field()

class MessageCreateSchema(BaseModel):
    sender_id: int = Field()
    text: str = Field()

class MessageUpdateSchema(BaseModel):
    text: Optional[str] = None