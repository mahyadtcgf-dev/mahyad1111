from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database.models import get_db, Base, engine, SessionLocal, User
from app.auth.router import router as auth_router
from app.subscriptions.router import router as sub_router
from app.auth.security import get_password_hash
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

# Include Routers
app.include_router(auth_router)
app.include_router(sub_router)

def create_initial_admin():
    """Creates a default admin user if one doesn't exist."""
    db = SessionLocal()
    try:
        admin_user = db.query(User).filter(User.username == "admin").first()
        if not admin_user:
            logger.info("Creating default admin user: admin/admin")
            new_admin = User(
                username="admin",
                password_hash=get_password_hash("admin"),
                email="admin@example.com",
                role="SUPER_ADMIN",
                is_active=True
            )
            db.add(new_admin)
            db.commit()
            logger.info("Default admin user created successfully.")
        else:
            logger.info("Admin user already exists.")
    except Exception as e:
        logger.error(f"Error creating initial admin: {e}")
    finally:
        db.close()

@app.on_event("startup")
async def startup_event():
    port = os.getenv("PORT", "8080")
    logger.info(f"Application is starting up on port {port}...")
    create_initial_admin()

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
