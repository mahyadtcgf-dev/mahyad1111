from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database.models import get_db, User
from app.auth.router import get_current_user
from pydantic import BaseModel, EmailStr
from typing import List
import uuid

router = APIRouter(prefix="/users", tags=["Users"])

class UserCreate(BaseModel):
    username: str
    password: str
    email: EmailStr
    role: str = "USER"

class UserOut(BaseModel):
    id: str
    username: str
    email: str
    role: str
    is_active: bool

@router.post("/", response_model=UserOut, status_code=status.HTTP_201_CREATED)
async def create_user(user_in: UserCreate, db: Session = Depends(get_db), admin=Depends(get_current_user)):
    if admin.role not in ["SUPER_ADMIN", "ADMIN"]:
        raise HTTPException(status_code=403, detail="Insufficient permissions")
    
    from app.auth.security import get_password_hash
    
    existing = db.query(User).filter((User.username == user_in.username) | (User.email == user_in.email)).first()
    if existing:
        raise HTTPException(status_code=400, detail="Username or email already exists")
    
    new_user = User(
        username=user_in.username,
        password_hash=get_password_hash(user_in.password),
        email=user_in.email,
        role=user_in.role,
        is_active=True
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@router.get("/", response_model=List[UserOut])
async def list_users(db: Session = Depends(get_db), admin=Depends(get_current_user)):
    if admin.role not in ["SUPER_ADMIN", "ADMIN"]:
        raise HTTPException(status_code=403, detail="Insufficient permissions")
    return db.query(User).all()

@router.delete("/{user_id}")
async def delete_user(user_id: str, db: Session = Depends(get_db), admin=Depends(get_current_user)):
    if admin.role not in ["SUPER_ADMIN", "ADMIN"]:
        raise HTTPException(status_code=403, detail="Insufficient permissions")
    
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    db.delete(user)
    db.commit()
    return {"detail": "User deleted"}
