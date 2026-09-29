from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database.models import get_db, Inbound, Server
from app.auth.router import get_current_user
from pydantic import BaseModel
from typing import List

router = APIRouter(prefix="/inbounds", tags=["Inbounds"])

class InboundCreate(BaseModel):
    server_id: str
    protocol: str
    port: int
    transport: str = "ws"
    path: str = "/"

class InboundOut(BaseModel):
    id: str
    protocol: str
    port: int
    transport: str
    path: str
    is_active: bool

@router.post("/", response_model=InboundOut, status_code=status.HTTP_201_CREATED)
async def create_inbound(inbound_in: InboundCreate, db: Session = Depends(get_db), admin=Depends(get_current_user)):
    if admin.role not in ["SUPER_ADMIN", "ADMIN"]:
        raise HTTPException(status_code=403, detail="Insufficient permissions")
    
    new_inbound = Inbound(
        server_id=inbound_in.server_id,
        protocol=inbound_in.protocol,
        port=inbound_in.port,
        transport=inbound_in.transport,
        path=inbound_in.path
    )
    db.add(new_inbound)
    db.commit()
    db.refresh(new_inbound)
    return new_inbound

@router.get("/", response_model=List[InboundOut])
async def list_inbounds(db: Session = Depends(get_db), admin=Depends(get_current_user)):
    if admin.role not in ["SUPER_ADMIN", "ADMIN"]:
        raise HTTPException(status_code=403, detail="Insufficient permissions")
    return db.query(Inbound).all()

@router.delete("/{inbound_id}")
async def delete_inbound(inbound_id: str, db: Session = Depends(get_db), admin=Depends(get_current_user)):
    if admin.role not in ["SUPER_ADMIN", "ADMIN"]:
        raise HTTPException(status_code=403, detail="Insufficient permissions")
    
    inbound = db.query(Inbound).filter(Inbound.id == inbound_id).first()
    if not inbound:
        raise HTTPException(status_code=404, detail="Inbound not found")
    
    db.delete(inbound)
    db.commit()
    return {"detail": "Inbound deleted"}
