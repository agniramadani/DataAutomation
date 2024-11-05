"""
Purpose:
--------
This module defines the database schema.

Note:
-----
- SQLAlchemy ORM is used for object-relational mapping.
- Relationships are defined for efficient data access across tables.
"""

from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime, timezone

Base = declarative_base()

class Patient(Base):
    __tablename__ = 'patients'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=True)
    date_of_birth = Column(DateTime, nullable=True)
    contact_info = Column(String, nullable=True)

    devices = relationship("DeviceData", back_populates="patient")
    feedback = relationship("UserFeedback", back_populates="patient")


class Device(Base):
    __tablename__ = 'devices'

    id = Column(Integer, primary_key=True, index=True)
    device_type = Column(String, nullable=False)
    model = Column(String, nullable=True)
    status = Column(String, default="active")

    data = relationship("DeviceData", back_populates="device")
    quality_checks = relationship("DataQualityCheck", back_populates="device")


class DeviceData(Base):
    __tablename__ = 'device_data'

    id = Column(Integer, primary_key=True, index=True)
    device_id = Column(Integer, ForeignKey('devices.id'))
    patient_id = Column(Integer, ForeignKey('patients.id'))
    timestamp = Column(DateTime, default=datetime.now(timezone.utc))
    parameter = Column(String, nullable=True)
    value = Column(Float, nullable=False)
    unit = Column(String, nullable=True)

    device = relationship("Device", back_populates="data")
    patient = relationship("Patient", back_populates="devices")


class DataQualityCheck(Base):
    __tablename__ = 'data_quality_checks'

    id = Column(Integer, primary_key=True, index=True)
    device_id = Column(Integer, ForeignKey('devices.id'))
    patient_id = Column(Integer, ForeignKey('patients.id'))
    timestamp = Column(DateTime, default=datetime.now(timezone.utc))
    missing_values = Column(Integer, default=0)
    duplicates = Column(Integer, default=0)
    outliers = Column(Integer, default=0)
    remarks = Column(String, nullable=True)

    device = relationship("Device", back_populates="quality_checks")


class UserFeedback(Base):
    __tablename__ = 'user_feedback'

    feedback_id = Column(Integer, primary_key=True, index=True)
    device_data_id = Column(Integer, ForeignKey('device_data.id'))
    patient_id = Column(Integer, ForeignKey('patients.id'))
    user_id = Column(String, nullable=False)
    timestamp = Column(DateTime, default=datetime.now(timezone.utc))
    feedback_text = Column(String, nullable=False)

    device_data = relationship("DeviceData")
    patient = relationship("Patient", back_populates="feedback")
