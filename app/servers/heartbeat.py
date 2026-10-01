from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database.models import get_db, Server, NodeStatus
from app.core.node_manager import node_manager
from pydantic import BaseModel

router = APIRouter(prefix="/heartbeat", tags=["Node Management"])

class HeartbeatPayload(BaseModel):
    node_id: str
    cpu: int
    memory: int
    bandwidth_in: int
    bandwidth_out: int
    active_connections: int

@router.post("/")
async def node_heartbeat(payload: HeartbeatPayload, db: Session = Depends(get_db)):
    server = db.query(Server).filter(Server.id == payload.node_id).first()
    if not server:
        raise HTTPException(status_code=404, detail="Node not registered")
    
    metrics = {
        "cpu": payload.cpu,
        "memory": payload.memory,
        "bandwidth_in": payload.bandwidth_in,
        "bandwidth_out": payload.bandwidth_out
    }
    
    await node_manager.update_node_status(db, server.id, NodeStatus.ONLINE, metrics)
    return {"status": "ok"}
