"""
API endpoints for accessing patient, device, and data records, with 
a background task to monitor database activity.
"""

from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from db_handler import SessionLocal
from models import Patient, Device, DataQualityCheck, UserFeedback
from tasks import monitor_db
import asyncio

app = FastAPI()

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
