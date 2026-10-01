
import asyncio
import httpx
import os
from app.main import app
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.database.models import Base, User, UserRole

async def run_tests():
    print("Starting Integration Tests...")
    
    # 1. Setup Database
    engine = create_engine(os.getenv("DATABASE_URL", "postgresql://postgres:postgres@localhost:5432/vpn_db"))
    SessionLocal = sessionmaker(bind=engine)
    db = SessionLocal()
    Base.metadata.create_all(bind=engine)
    
    # 2. Create Test Admin
    admin = User(username="test_admin", password_hash="hashed_pwd", role=UserRole.SUPER_ADMIN)
    db.add(admin)
    db.commit()
    
    # 3. Test Health Endpoint
    async with httpx.AsyncClient(app=app, base_url="http://test") as ac:
        res = await ac.get("/health")
        print(f"Health Check: {'PASS' if res.status_code == 200 else 'FAIL'}")
        
        res = await ac.get("/ready")
        print(f"Readiness Check: {'PASS' if res.status_code == 200 else 'FAIL'}")

    print("Tests Completed.")

if __name__ == "__main__":
    asyncio.run(run_tests())
