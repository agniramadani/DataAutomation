"""
This script generates fake patient and devices for testing.

Run this script to populate the database with sample data for testing.
"""

from faker import Faker
from models import Patient, Device, User
from db_handler import SessionLocal
import random
from passlib.context import CryptContext

fake = Faker()
session = SessionLocal()

pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")

def create_fake_patients(num_patients=10):
    patients = []
    for _ in range(num_patients):
        patient = Patient(
            name=fake.name(),
            date_of_birth=fake.date_of_birth(minimum_age=18, maximum_age=90),
            contact_info=fake.phone_number()
        )
        session.add(patient)
        patients.append(patient)
    session.commit()
    return patients

def create_fake_devices(num_devices=5):
    devices = []
    device_types = ["Heart Monitor", "Blood Pressure Monitor", "Temperature Sensor", "Oximeter", "ECG"]
    for _ in range(num_devices):
        device = Device(
            device_type=random.choice(device_types),
            model=fake.bothify(text="Model-####"),
            status="active"
        )
        session.add(device)
        devices.append(device)
    session.commit()
    return devices

def create_admin_user():
    # Note: Using 'admin' as username and password is for demonstration purposes only!
    admin_user = User(
        full_name="Admin User",
        username="admin",
        password=pwd_context.hash("admin")
    )
    session.add(admin_user)
    session.commit()

def main():
    create_fake_patients()
    create_fake_devices()
    create_admin_user()

    print("Fake data generated successfully!")

if __name__ == "__main__":
    main()
