from sqlalchemy import Column, String, Integer, Enum, DateTime, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from app.db.session import Base
import enum

class UserRole(str, enum.Enum):
    user = "user"
    recruiter = "recruiter"

class Prefix(str, enum.Enum):
    mr = "Mr"
    ms = "Ms"
    miss = "Miss"

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    password = Column(String, nullable=False)
    role = Column(Enum(UserRole), default=UserRole.user)
    prefix = Column(Enum(Prefix), nullable=True)
    phone_number = Column(String, nullable=True)
    address = Column(String, nullable=True)
    city = Column(String, nullable=True)
    state = Column(String, nullable=True)
    pincode = Column(String, nullable=True)
    nationality = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
