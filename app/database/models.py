from sqlalchemy import create_engine, Column, String, Boolean, Integer, DateTime, ForeignKey, BigInteger, Enum, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
import os
import uuid
from datetime import datetime
from enum import Enum as PyEnum

# Environment setup
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres:postgres@localhost:5432/vpn_db")

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class UserRole(str, PyEnum):
    SUPER_ADMIN = "SUPER_ADMIN"
    ADMIN = "ADMIN"
    OPERATOR = "OPERATOR"
    VIEWER = "VIEWER"
    USER = "USER"

class User(Base):
    __tablename__ = "users"
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    username = Column(String, unique=True, index=True, nullable=False)
    password_hash = Column(String, nullable=False)
    email = Column(String, unique=True, index=True)
    role = Column(String, default=UserRole.USER)
    is_active = Column(Boolean, default=True)
    two_fa_secret = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    subscriptions = relationship("Subscription", back_populates="user")

class Server(Base):
    __tablename__ = "servers"
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    label = Column(String, nullable=False)
    endpoint = Column(String, nullable=False)
    port = Column(Integer, nullable=False)
    location = Column(String)
    protocols = Column(JSON) # List of supported protocols
    status = Column(String, default="ONLINE")
    last_seen = Column(DateTime, default=datetime.utcnow)

class Subscription(Base):
    __tablename__ = "subscriptions"
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String, ForeignKey("users.id"))
    token = Column(String, unique=True, index=True, nullable=False)
    traffic_limit = Column(BigInteger, default=0) # bytes
    traffic_used = Column(BigInteger, default=0)
    expiration_date = Column(DateTime, nullable=True)
    device_limit = Column(Integer, default=1)
    status = Column(String, default="ACTIVE")
    
    user = relationship("User", back_populates="subscriptions")
    configs = relationship("Configuration", back_populates="subscription")

class Configuration(Base):
    __tablename__ = "configurations"
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    sub_id = Column(String, ForeignKey("subscriptions.id"))
    server_id = Column(String, ForeignKey("servers.id"))
    protocol = Column(String, nullable=False)
    config_data = Column(JSON, nullable=False)
    link = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    subscription = relationship("Subscription", back_populates="configs")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
