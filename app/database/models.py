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
    status = Column(String, default="ONLINE")
    last_seen = Column(DateTime, default=datetime.utcnow)
    
    inbounds = relationship("Inbound", back_populates="server")

class Inbound(Base):
    __tablename__ = "inbounds"
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    server_id = Column(String, ForeignKey("servers.id"))
    protocol = Column(String, nullable=False) # vless, vmess, trojan, shadowsocks
    port = Column(Integer, nullable=False)
    transport = Column(String, default="ws") # ws, grpc, tcp, xhttp
    path = Column(String, default="/")
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    server = relationship("Server", back_populates="inbounds")
    configs = relationship("Configuration", back_populates="inbound")

class Configuration(Base):
    __tablename__ = "configurations"
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    sub_id = Column(String, ForeignKey("subscriptions.id"))
    server_id = Column(String, ForeignKey("servers.id"))
    inbound_id = Column(String, ForeignKey("inbounds.id")) # Added reference to Inbound
    protocol = Column(String, nullable=False)
    config_data = Column(JSON, nullable=False)
    link = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    subscription = relationship("Subscription", back_populates="configs")
    inbound = relationship("Inbound", back_populates="configs")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
