from typing import Optional
from pydantic import BaseModel, EmailStr, Field
from typing import Literal

ADMIN = Literal["Admin"]
PARTICIPANT = Literal["Participant"]
MemberRole = Literal["Participant", "Admin"]

class MemberSchema(BaseModel):
    id: int = Field()
    user_id: int = Field()
    chat_id: int = Field()
    role: MemberRole = "Participant"

class MemberCreateSchema(BaseModel):
    user_id: int = Field()
    chat_id: int = Field()
    role: MemberRole = "Participant"

class MemberUpdateSchema(BaseModel):
    user_id: int = Field()
    chat_id: int = Field()
    role: MemberRole = "Participant"

class MembershipSchema(MemberCreateSchema):
    pass
