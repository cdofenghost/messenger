from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from ..database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    email = Column(String, unique=True)
    bio = Column(String)
    status = Column(String)
    hashed_password = Column(String)

    participations = relationship("Participant", back_populates="user", cascade="all, delete")