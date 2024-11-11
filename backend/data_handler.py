"""
This script handles loading data from a CSV file,
flags records as `reported` (true/false) if present in DataQualityCheck table, 
and returns JSON.
"""

import pandas as pd
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from models import DataQualityCheck

def get_all_data(db: Session):
    try:
        # Load data from CSV file
        data = pd.read_csv('../data.csv')

        # Replace NaN values with None
        data = data.where(pd.notnull(data), None)

        # Get the list of record_ids in DataQualityCheck
        reported_record_ids = {record.record_id for record in db.query(DataQualityCheck.record_id).all()}

        # Add a "reported" column to the DataFrame if record_id is in DataQualityCheck
        data['reported'] = data['record_id'].apply(lambda x: x in reported_record_ids)

        # Convert data to JSON format
        data_json = data.to_dict(orient="records")

        # We return JSON response
        return JSONResponse(content=data_json)

    except FileNotFoundError:
        return JSONResponse(content={"error": "File not found"}, status_code=404)
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)
