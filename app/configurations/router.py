from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database.models import get_db, Configuration, Subscription, Server, User
from app.auth.router import get_current_user
from app.protocols.registry import registry
from pydantic import BaseModel
import uuid

router = APIRouter(prefix="/configs", tags=["Configurations"])

class ConfigCreate(BaseModel):
    user_id: str
    server_id: str
    protocol: str # vless, vmess, trojan
    params: dict = {}

@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_config(config_in: ConfigCreate, db: Session = Depends(get_db), admin=Depends(get_current_user)):
    if admin.role not in ["SUPER_ADMIN", "ADMIN"]:
        raise HTTPException(status_code=403, detail="Insufficient permissions")
    
    # 1. Validate Protocol
    handler = registry.get(config_in.protocol)
    if not handler:
        raise HTTPException(status_code=400, detail=f"Protocol {config_in.protocol} not supported")
    
    # 2. Get Server
    server = db.query(Server).filter(Server.id == config_in.server_id).first()
    if not server:
        raise HTTPException(status_code=404, detail="Server not found")
    
    # 3. Get or Create Subscription for User
    sub = db.query(Subscription).filter(Subscription.user_id == config_in.user_id).first()
    if not sub:
        sub = Subscription(
            user_id=config_in.user_id,
            token=str(uuid.uuid4())[:12],
            status="ACTIVE"
        )
        db.add(sub)
        db.commit()
        db.refresh(sub)
    
    # 4. Generate Protocol-specific Data
    params = {**config_in.params, "endpoint": server.endpoint, "port": server.port}
    proto_data = await handler.create(config_in.user_id, params)
    
    # 5. Generate Final Link
    final_params = {**proto_data, "endpoint": server.endpoint, "port": server.port, "label": server.label}
    link = handler.generate_link(final_params)
    
    # 6. Save to DB
    new_config = Configuration(
        sub_id=sub.id,
        server_id=server.id,
        protocol=config_in.protocol,
        config_data=final_params,
        link=link
    )
    db.add(new_config)
    db.commit()
    db.refresh(new_config)
    
    return {"config_id": new_config.id, "link": link, "sub_token": sub.token}
