"""
Purpose:
--------
This script checks for data quality issues in CSV files, including missing values and out-of-range values,
and logs unique issues to the database if they are not already recorded.
"""

import pandas as pd
from datetime import datetime, timezone
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError
from config import DATABASE_URL
from models import DataQualityCheck

# Database setup
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)

# Define acceptable ranges for different parameters
PARAMETER_RANGES = {
    "heart_rate": (60, 100),
    "blood_oxygen": (90, 100),
    "ecg": (-2, 2)
}

def check_data_quality():
    # Load the CSV data
    try:
        # Define the path to the CSV file
        data = pd.read_csv('../data.csv')
    except FileNotFoundError:
        print("CSV file not found.")
        return

    # Initialize a list to store unique quality check issues
    quality_issues = []

    session = SessionLocal()
    try:
        for index, row in data.iterrows():
            missing_values = []
            outliers = []
            record_id = row["record_id"]
            patient_id = row["patient_id"]
            device_id = row["device_id"]

            # Check for missing data
            if pd.isna(row["parameter"]):
                missing_values.append("parameter")
            if pd.isna(row["value"]):
                missing_values.append("value")
            if pd.isna(row["unit"]):
                missing_values.append("unit")

            # Check for out-of-range values if parameter and value are present
            parameter = row.get("parameter")
            value = row.get("value")

            if parameter in PARAMETER_RANGES and pd.notna(value):
                try:
                    # Convert value to float for comparison
                    numeric_value = float(value)
                    min_val, max_val = PARAMETER_RANGES[parameter]
                    if not (min_val <= numeric_value <= max_val):
                        outliers.append(f"{parameter} out of range: {value} (expected {min_val}-{max_val})")
                except ValueError:
                    outliers.append(f"{parameter} has non-numeric value: {value}")

            # Skip entry if no issues are found
            if not missing_values and not outliers:
                continue

            # Check if a record already exists for this patient and device
            existing_check = session.query(DataQualityCheck).filter_by(
                device_id=device_id, patient_id=patient_id
            ).first()

            if existing_check is None:
                # Prepare the data quality issue for insertion
                quality_issue = DataQualityCheck(
                    record_id=record_id,
                    device_id=device_id,
                    patient_id=patient_id,
                    timestamp=datetime.now(timezone.utc),
                    missing_values=len(missing_values),
                    outliers=len(outliers),
                    remarks = "Issue(s): " + "; ".join(missing_values + outliers)
                )
                quality_issues.append(quality_issue)

        # Insert all unique quality issues into the database
        if quality_issues:
            try:
                session.add_all(quality_issues)
                session.commit()
            except SQLAlchemyError as e:
                session.rollback()
                print("Failed to log quality issues:", e)
    finally:
        session.close()

if __name__ == "__main__":
    check_data_quality()
