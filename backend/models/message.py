from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from ..database import Base

class Message(Base):
    __tablename__ = "messages"

    id = Column(Integer, primary_key=True, index=True)
    sender_id = Column(Integer, ForeignKey("participants.id", ondelete="CASCADE"))
    text = Column(String)

    sender = relationship("Participant", foreign_keys=[sender_id], cascade="all, delete", back_populates="messages")
    # attachments

