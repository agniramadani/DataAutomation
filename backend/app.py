"""
API endpoints for accessing patient, device, and data records, with 
a background task to monitor database activity.
"""

import asyncio

from fastapi import Depends, FastAPI, HTTPException, status, Request
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

from auth_handler import login
from db_handler import SessionLocal
from models import DataQualityCheck, Device, Patient, User, UserFeedback, UserAuthentication
from tasks import monitor_db
from data_handler import get_all_data

app = FastAPI()

# NOTE: Allowing any port on localhost for development purposes only.
# WARNING: In production, this should be restricted to specific origins to ensure security.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Start the background task when the application starts
@app.on_event("startup")
async def start_monitoring():
    asyncio.create_task(monitor_db())

@app.post("/api/login")
async def api_login(request: Request, db: Session = Depends(get_db)):
    body = await request.json()
    username = body.get("username")
    password = body.get("password")
    
    if not username or not password:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username and password are required",
        )
    
    token = login(db, username, password)
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password",
        )
    
    return {"access_token": token, "token_type": "bearer"}

@app.get("/api/patients")
async def get_patients(db: Session = Depends(get_db)):
    patients = db.query(Patient).all()
    return patients

@app.get("/api/devices")
async def get_devices(db: Session = Depends(get_db)):
    devices = db.query(Device).all()
    return devices

@app.get("/api/data-quality-checks")
async def get_data_quality_checks(db: Session = Depends(get_db)):
    data_quality_checks = db.query(DataQualityCheck).all()
    return data_quality_checks

@app.get("/api/user-feedback")
async def get_user_feedback(db: Session = Depends(get_db)):
    user_feedback = db.query(UserFeedback).all()
    return user_feedback

@app.get("/api/all-data")
async def api_get_all_data(db: Session = Depends(get_db)):
    return get_all_data(db)
