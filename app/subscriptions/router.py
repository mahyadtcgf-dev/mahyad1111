from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database.models import get_db, Subscription, Configuration, Server
from app.auth.security import decode_access_token
from fastapi.security import OAuth2PasswordBearer
from app.core.config import settings
import base64

router = APIRouter(prefix="/subscriptions", tags=["Subscriptions"])
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

@router.get("/{token}")
async def get_subscription(token: str, db: Session = Depends(get_db)):
    """
    Public endpoint for VPN clients to fetch their config list.
    """
    sub = db.query(Subscription).filter(Subscription.token == token).first()
    if not sub or sub.status != "ACTIVE":
        raise HTTPException(status_code=404, detail="Subscription not found or inactive")
    
    configs = db.query(Configuration).filter(Configuration.sub_id == sub.id).all()
    
    # Generate a simple text list of links (Standard for many VPN clients)
    links = [config.link for config in configs]
    config_text = "\n".join(links)
    
    # Return as Base64 for compatibility with some clients, or plain text
    return {
        "token": token,
        "status": sub.status,
        "traffic_used": sub.traffic_used,
        "traffic_limit": sub.traffic_limit,
        "links": links,
        "raw": config_text,
        "base64": base64.b64encode(config_text.encode()).decode()
    }
