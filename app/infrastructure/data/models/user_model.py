from sqlalchemy import Column, Integer, String, DateTime, Boolean, Enum as sqlEnum, Text
from sqlalchemy.sql import func
import enum
from app.infrastructure.data.database import Base

class UserType(enum.Enum):
    TENANT = "tenant"
    LANDLORD = "landlord" 
    AGENT = "agent"
    ADMIN = "admin" 

class UserRole(enum.Enum):
    USER = "user"
    ADMIN = "admin"
    SUPER_ADMIN = "super_admin"

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    username = Column(String, unique=True, index=True, nullable=True)
    hashed_password = Column(String, nullable=False)
    
    # User type and status
    user_type =Column(sqlEnum(UserType, name='usertype', values_callable=lambda x: [m.value for m in x]), nullable=False)
    role =Column(sqlEnum(UserRole, name='userrole', values_callable=lambda x: [m.value for m in x]), nullable=True)
    
    is_active = Column(Boolean, default=True)
    is_verified = Column(Boolean, default=False)
    
    # Personal info
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    phone = Column(String, nullable=True)
    
    # Profile
    bio = Column(Text, nullable=True)
    avatar_url = Column(String, nullable=True)
    
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    last_login = Column(DateTime(timezone=True), nullable=True)