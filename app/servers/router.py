from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database.models import get_db, Server, NodeStatus
from app.auth.dependencies import is_admin
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

router = APIRouter(prefix="/servers", tags=["Servers"])

class ServerCreate(BaseModel):
    label: str
    endpoint: str
    port: int
    region: Optional[str] = None
    provider: Optional[str] = None
    public_key: Optional[str] = None

class ServerOut(BaseModel):
    id: str
    label: str
    endpoint: str
    port: int
    region: Optional[str]
    provider: Optional[str]
    status: str
    last_seen: datetime

    class Config:
        from_attributes = True

@router.post("/", response_model=ServerOut, status_code=status.HTTP_201_CREATED)
async def create_server(server_in: ServerCreate, db: Session = Depends(get_db), admin=Depends(is_admin)):
    new_server = Server(
        label=server_in.label,
        endpoint=server_in.endpoint,
        port=server_in.port,
        region=server_in.region,
        provider=server_in.provider,
        public_key=server_in.public_key,
        status=NodeStatus.UNKNOWN
    )
    db.add(new_server)
    db.commit()
    db.refresh(new_server)
    return new_server

@router.get("/", response_model=List[ServerOut])
async def list_servers(db: Session = Depends(get_db), admin=Depends(is_admin)):
    return db.query(Server).all()

@router.get("/{server_id}", response_model=ServerOut)
async def get_server(server_id: str, db: Session = Depends(get_db), admin=Depends(is_admin)):
    server = db.query(Server).filter(Server.id == server_id).first()
    if not server:
        raise HTTPException(status_code=404, detail="Server not found")
    return server

@router.delete("/{server_id}")
async def delete_server(server_id: str, db: Session = Depends(get_db), admin=Depends(is_admin)):
    server = db.query(Server).filter(Server.id == server_id).first()
    if not server:
        raise HTTPException(status_code=404, detail="Server not found")
    db.delete(server)
    db.commit()
    return {"detail": "Server deleted"}
