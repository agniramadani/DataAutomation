"""
This module allows saving user feedback to the database.
"""

from sqlalchemy.orm import Session
from models import UserFeedback

def save_feedback(db: Session, record_id: int, device_id: int, patient_id: int, user_id: int, feedback_text: str):
    feedback_entry = UserFeedback(
        record_id=record_id,
        device_id=device_id,
        patient_id=patient_id,
        user_id=user_id,
        feedback_text=feedback_text
    )
    db.add(feedback_entry)
    db.commit()
