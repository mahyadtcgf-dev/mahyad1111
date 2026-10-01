from sqlalchemy import create_engine, Column, String, Boolean, Integer, DateTime, ForeignKey, BigInteger, Enum, JSON, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
import os
import uuid
from datetime import datetime
from enum import Enum as PyEnum

# Environment setup
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres:***@localhost:5432/vpn_db")

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class UserRole(str, PyEnum):
    SUPER_ADMIN = "SUPER_ADMIN"
    ADMIN = "ADMIN"
    OPERATOR = "OPERATOR"
    VIEWER = "VIEWER"
    USER = "USER"

class NodeStatus(str, PyEnum):
    ONLINE = "ONLINE"
    OFFLINE = "OFFLINE"
    DEGRADED = "DEGRADED"
    MAINTENANCE = "MAINTENANCE"
    UNKNOWN = "UNKNOWN"

class PlanStatus(str, PyEnum):
    ACTIVE = "ACTIVE"
    INACTIVE = "INACTIVE"

class SubscriptionStatus(str, PyEnum):
    ACTIVE = "ACTIVE"
    EXPIRED = "EXPIRED"
    SUSPENDED = "SUSPENDED"

class ConfigStatus(str, PyEnum):
    ACTIVE = "ACTIVE"
    EXPIRED = "EXPIRED"
    REVOKED = "REVOKED"
    DISABLED = "DISABLED"

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
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    subscriptions = relationship("Subscription", back_populates="user")
    devices = relationship("Device", back_populates="user")

class Server(Base):
    __tablename__ = "servers"
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    label = Column(String, nullable=False)
    endpoint = Column(String, nullable=False)
    port = Column(Integer, nullable=False)
    region = Column(String)
    provider = Column(String)
    status = Column(String, default=NodeStatus.UNKNOWN)
    public_key = Column(String, nullable=True)
    last_seen = Column(DateTime, default=datetime.utcnow)
    cpu_usage = Column(Integer, default=0)
    memory_usage = Column(Integer, default=0)
    bandwidth_in = Column(BigInteger, default=0)
    bandwidth_out = Column(BigInteger, default=0)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
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

class Subscription(Base):
    __tablename__ = "subscriptions"
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String, ForeignKey("users.id"))
    plan_id = Column(String, ForeignKey("plans.id"), nullable=True)
    token = Column(String, unique=True, index=True, nullable=False)
    traffic_limit = Column(BigInteger, default=0) # bytes
    traffic_used = Column(BigInteger, default=0)
    expiration_date = Column(DateTime, nullable=True)
    device_limit = Column(Integer, default=1)
    status = Column(String, default=SubscriptionStatus.ACTIVE)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    user = relationship("User", back_populates="subscriptions")
    configs = relationship("Configuration", back_populates="subscription")

class Configuration(Base):
    __tablename__ = "configurations"
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    sub_id = Column(String, ForeignKey("subscriptions.id"))
    server_id = Column(String, ForeignKey("servers.id"))
    inbound_id = Column(String, ForeignKey("inbounds.id"))
    protocol = Column(String, nullable=False)
    config_data = Column(JSON, nullable=False)
    link = Column(String, nullable=False)
    status = Column(String, default=ConfigStatus.ACTIVE)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    subscription = relationship("Subscription", back_populates="configs")
    inbound = relationship("Inbound", back_populates="configs")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

class Plan(Base):
    __tablename__ = "plans"
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String, nullable=False)
    description = Column(Text)
    traffic_limit = Column(BigInteger, default=0) # 0 for unlimited
    device_limit = Column(Integer, default=1)
    duration_days = Column(Integer, nullable=False)
    price = Column(Integer, default=0)
    status = Column(String, default=PlanStatus.ACTIVE)
    created_at = Column(DateTime, default=datetime.utcnow)

class Device(Base):
    __tablename__ = "devices"
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String, ForeignKey("users.id"))
    device_name = Column(String, nullable=False)
    platform = Column(String)
    last_ip = Column(String)
    last_seen = Column(DateTime, default=datetime.utcnow)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    user = relationship("User", back_populates="devices")

class AuditLog(Base):
    __tablename__ = "audit_logs"
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String, ForeignKey("users.id"), nullable=True)
    action = Column(String, nullable=False)
    resource = Column(String)
    resource_id = Column(String)
    old_value = Column(JSON, nullable=True)
    new_value = Column(JSON, nullable=True)
    ip_address = Column(String)
    timestamp = Column(DateTime, default=datetime.utcnow)

class TrafficUsage(Base):
    __tablename__ = "traffic_usage"
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    sub_id = Column(String, ForeignKey("subscriptions.id"))
    upload_bytes = Column(BigInteger, default=0)
    download_bytes = Column(BigInteger, default=0)
    timestamp = Column(DateTime, default=datetime.utcnow)
