from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database.models import get_db, Server
from app.auth.router import get_current_user
from pydantic import BaseModel
from typing import List

router = APIRouter(prefix="/servers", tags=["Servers"])

class ServerCreate(BaseModel):
    label: str
    endpoint: str
    port: int
    location: str
    protocols: list[str]

class ServerOut(BaseModel):
    id: str
    label: str
    endpoint: str
    port: int
    location: str
    status: str

@router.post("/", response_model=ServerOut, status_code=status.HTTP_201_CREATED)
async def create_server(server_in: ServerCreate, db: Session = Depends(get_db), admin=Depends(get_current_user)):
    if admin.role not in ["SUPER_ADMIN", "ADMIN"]:
        raise HTTPException(status_code=403, detail="Insufficient permissions")
    
    new_server = Server(
        label=server_in.label,
        endpoint=server_in.endpoint,
        port=server_in.port,
        location=server_in.location,
        protocols=server_in.protocols
    )
    db.add(new_server)
    db.commit()
    db.refresh(new_server)
    return new_server

@router.get("/", response_model=List[ServerOut])
async def list_servers(db: Session = Depends(get_db), admin=Depends(get_current_user)):
    if admin.role not in ["SUPER_ADMIN", "ADMIN"]:
        raise HTTPException(status_code=403, detail="Insufficient permissions")
    return db.query(Server).all()
