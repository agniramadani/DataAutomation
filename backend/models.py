"""
Purpose:
--------
This module defines the database schema.

Note:
-----
- SQLAlchemy ORM is used for object-relational mapping.
- Relationships are defined for efficient data access across tables.
"""

from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime, timezone

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String, nullable=False)
    username = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    
    feedback = relationship("UserFeedback", back_populates="user")
    authentications = relationship("UserAuthentication", back_populates="user")


class Patient(Base):
    __tablename__ = 'patients'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=True)
    date_of_birth = Column(DateTime, nullable=True)
    contact_info = Column(String, nullable=True)

    quality_checks = relationship("DataQualityCheck", back_populates="patient") 
    feedback = relationship("UserFeedback", back_populates="patient")


class Device(Base):
    __tablename__ = 'devices'

    id = Column(Integer, primary_key=True, index=True)
    device_type = Column(String, nullable=False)
    model = Column(String, nullable=True)
    status = Column(String, default="active")

    quality_checks = relationship("DataQualityCheck", back_populates="device")
    feedback = relationship("UserFeedback", back_populates="device")


class UserAuthentication(Base):
    __tablename__ = 'user_authentications'

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    auth_token = Column(String, unique=True, nullable=False)
    created_at = Column(DateTime, default=datetime.now(timezone.utc))

    user = relationship("User", back_populates="authentications")


class DataQualityCheck(Base):
    __tablename__ = 'data_quality_checks'

    id = Column(Integer, primary_key=True, index=True)
    record_id = Column(Integer)
    device_id = Column(Integer, ForeignKey('devices.id'))
    patient_id = Column(Integer, ForeignKey('patients.id'))
    timestamp = Column(DateTime, default=datetime.now(timezone.utc))
    missing_values = Column(Integer, default=0)
    outliers = Column(Integer, default=0)
    remarks = Column(String, nullable=True)

    device = relationship("Device", back_populates="quality_checks")
    patient = relationship("Patient", back_populates="quality_checks")


class UserFeedback(Base):
    __tablename__ = 'user_feedback'

    feedback_id = Column(Integer, primary_key=True, index=True)
    record_id = Column(Integer)
    device_id = Column(Integer, ForeignKey('devices.id'))
    patient_id = Column(Integer, ForeignKey('patients.id'))
    user_id = Column(Integer, ForeignKey('users.id'))
    timestamp = Column(DateTime, default=datetime.now(timezone.utc))
    feedback_text = Column(String, nullable=False)

    patient = relationship("Patient", back_populates="feedback")
    user = relationship("User", back_populates="feedback")
    device = relationship("Device", back_populates="feedback")
