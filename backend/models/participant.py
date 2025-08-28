from sqlalchemy import ( 
    Column, Integer, String, ForeignKey, 
    UniqueConstraint,
)
from sqlalchemy.orm import relationship
from ..database import Base

class Participant(Base):
    __tablename__ = "participants"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"))
    chat_id = Column(Integer, ForeignKey("chats.id", ondelete="CASCADE"))

    user = relationship("User", foreign_keys=[user_id], back_populates="participations")
    chat = relationship("Chat", foreign_keys=[chat_id], back_populates="participants")
    messages = relationship("Message", cascade="all, delete", back_populates="sender")

    __table_args__ = (UniqueConstraint('user_id', 'chat_id', name='_user_participation_uc'),)