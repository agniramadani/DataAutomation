"""
Purpose:
--------
This module provides background tasks to monitor database status and activity. 

Note:
-----
- Scheduled tasks use asynchronous processing to avoid blocking primary workflows.
"""

import asyncio
from db_handler import check_data_quality

# Global variable to store the latest monitoring result
latest_result = {"status": "No data yet"}

async def monitor_db():
    global latest_result
    while True:
        # Run data quality check and update the latest result
        latest_result = check_data_quality()
        await asyncio.sleep(3600)  # Check every hour
