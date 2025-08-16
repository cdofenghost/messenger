from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from ..database import Base

class Participant(Base):
    __table__ = "participants"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"))
    chat_id = Column(Integer, ForeignKey("chats.id", ondelete="CASCADE"))

    user = relationship("User", foreign_keys=[user_id], cascade="all, delete", back_populates="participations")
    chat = relationship("Chat", foreign_keys=[chat_id], cascade="all, delete", back_populates="participants")
