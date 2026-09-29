from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database.models import get_db, Base, engine
import logging

# Create tables on startup
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Professional VPN Management Panel",
    description="A high-performance VPN management system for Railway.app",
    version="1.0.0"
)

@app.get("/health")
async def health_check():
    return {"status": "ok", "version": "1.0.0"}

@app.get("/ready")
async def ready_check(db: Session = Depends(get_db)):
    try:
        # Simple query to check DB connectivity
        db.execute("SELECT 1")
        return {"status": "ready"}
    except Exception as e:
        raise HTTPException(status_code=503, detail=f"Database not ready: {str(e)}")

# Other API routes will be added here (Auth, Users, etc.)
