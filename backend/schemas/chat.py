from typing import Optional

from pydantic import BaseModel, Field
from datetime import datetime

from fastapi import Query

from typing import Literal

class ChatSchema(BaseModel):
    id: int = Field()
    name: str = Field()
    type: str = Field()
    created_at: datetime = Field()
    updated_at: datetime = Field()

Type = Literal["Direct Messages", "Private", "Public"]
class ChatCreateSchema(BaseModel):
    name: Optional[str] = None
    type: Type = "Private"


class ChatUpdateSchema(BaseModel):
    name: Optional[str] = None
    type: Optional[Type] = None

