"""
API endpoints for accessing patient, device, and data records, with 
a background task to monitor database activity.
"""

import asyncio
from fastapi import Depends, FastAPI, HTTPException, status, Request
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from feedback_handler import save_feedback
from contextlib import asynccontextmanager

from auth_handler import login
from db_handler import SessionLocal
from models import DataQualityCheck, Device, Patient, UserFeedback, UserAuthentication
from tasks import monitor_db
from data_handler import get_all_data

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Start the background task
    task = asyncio.create_task(monitor_db())
    yield
    # Cancel the background task on shutdown
    task.cancel()

app = FastAPI(lifespan=lifespan)

# Allow any port on localhost for development only. 
# WARNING: Restrict origins in production for security.
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
    
    result = login(db, username, password)
    if result is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password",
        )

    token, user_id = result
    return {"token": token, "user_id": user_id}

def verify_token(request: Request, db: Session = Depends(get_db)):
    # Extract the token
    auth_token = request.headers.get("Authorization")

    # Validate token and existence in database
    if auth_token and db.query(UserAuthentication).filter_by(auth_token=auth_token).first():
        return status.HTTP_200_OK
    
    # Token is either missing or invalid
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid or missing token"
    )

@app.get("/api/patients", dependencies=[Depends(verify_token)])
async def get_patients(db: Session = Depends(get_db)):
    return db.query(Patient).all()

@app.get("/api/devices", dependencies=[Depends(verify_token)])
async def get_devices(db: Session = Depends(get_db)):
    return db.query(Device).all()

@app.get("/api/data-quality-checks", dependencies=[Depends(verify_token)])
async def get_data_quality_checks(db: Session = Depends(get_db)):
    return db.query(DataQualityCheck).all()

@app.get("/api/all-data", dependencies=[Depends(verify_token)])
async def api_get_all_data(db: Session = Depends(get_db)):
    return get_all_data(db)

@app.post("/api/feedback", dependencies=[Depends(verify_token)])
async def create_feedback(request: Request, db: Session = Depends(get_db)):
    body = await request.json()
    user_id = body.get("user_id")
    record_id = body.get("record_id")
    device_id = body.get("device_id")
    patient_id = body.get("patient_id")
    feedback_text = body.get("feedback_text")
    
    if not feedback_text:
        raise HTTPException(status_code=400, detail="Feedback text is required.")
    
    save_feedback(db, record_id, device_id, patient_id, user_id, feedback_text)
    return status.HTTP_201_CREATED

@app.get("/api/all-feedbacks", dependencies=[Depends(verify_token)])
async def get_all_feedback(db: Session = Depends(get_db)):
    return db.query(UserFeedback).all()
