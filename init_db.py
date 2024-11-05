"""
Purpose:
--------
This script initializes the database connection and creates tables based on 
the schema defined in the models.
"""

from sqlalchemy import create_engine
from models import Base
from config import DATABASE_URL

# Setup database connection
engine = create_engine(DATABASE_URL)

# Create tables
Base.metadata.create_all(engine)
print("Tables created successfully.")
