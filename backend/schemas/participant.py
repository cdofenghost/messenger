from typing import Optional
from pydantic import BaseModel, EmailStr, Field

class ParticipantSchema(BaseModel):
    id: int = Field()
    user_id: int = Field()
    chat_id: int = Field()

class ParticipantCreateSchema(BaseModel):
    user_id: int = Field()
    chat_id: int = Field()

class ParticipationSchema(ParticipantCreateSchema):
    pass
