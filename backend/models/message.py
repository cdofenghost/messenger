from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, func
from sqlalchemy.orm import relationship
from ..database import Base

class Message(Base):
    __tablename__ = "messages"

    id = Column(Integer, primary_key=True, index=True)
    sender_id = Column(Integer, ForeignKey("members.id", ondelete="CASCADE"))
    text = Column(String)
    created_at = Column(DateTime(timezone=True), server_default=func.now()) 
    edited_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now()) 

    sender = relationship("Member", foreign_keys=[sender_id], cascade="all, delete", back_populates="messages")
    # attachments

