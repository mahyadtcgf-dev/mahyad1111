from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database.models import get_db, Base, engine
import logging
import os

# Setup logging to help debug "Application failed to respond"
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("vpn-panel")

# Create tables on startup
try:
    Base.metadata.create_all(bind=engine)
    logger.info("Database tables created successfully.")
except Exception as e:
    logger.error(f"Critical error creating database tables: {e}")

app = FastAPI(
    title="Professional VPN Management Panel",
    description="A high-performance VPN management system for Railway.app",
    version="1.0.0"
)

@app.on_event("startup")
async def startup_event():
    port = os.getenv("PORT", "8080")
    logger.info(f"Application is starting up on port {port}...")

@app.get("/health")
async def health_check():
    logger.info("Health check requested")
    return {"status": "ok", "version": "1.0.0"}

@app.get("/ready")
async def ready_check(db: Session = Depends(get_db)):
    try:
        db.execute("SELECT 1")
        return {"status": "ready"}
    except Exception as e:
        logger.error(f"Readiness check failed: {e}")
        raise HTTPException(status_code=503, detail=f"Database not ready: {str(e)}")

# Other API routes will be added here (Auth, Users, etc.)
