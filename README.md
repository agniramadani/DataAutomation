# DataAutomation
A data automation project for a Basel-based pharma company, enabling data validation, event logging, and anomaly alerts, while allowing users to provide feedback for continuous improvement.

## Roadmap
- Screenshot

- Prerequisites

- Getting Started

- App Overview

- Author

## Screenshot
![Screenshot](Screenshot.png)

## Prerequisites
- Python 3
- FastAPI
- SQLite
- React
- Vite

## Getting Started

### Install Backend Dependencies

```bash
pip install -r requirements.txt
```

### Set Up the Database
```bash
cd backend && python3 init_db.py
```

### Generate Fake Data (Optional)
```bash
cd backend && python3 fake_data.py
```

### Start the Backend Server
```bash
cd backend && uvicorn app:app --reload   
```

### Set Up the Frontend
```bash
cd frontend && yarn install
```

### Run the Frontend Application
```bash
cd frontend && yarn dev
```

## App Overview
### Setup and Initial Login
After setting up the backend and generating fake data for demonstration purposes, you can log in using the following credentials, which are intended for testing only:

**Username:** `admin`

**Password:** `admin`

*Important*: These credentials are insecure. Replace them with a secure user setup for real-world use.

### Key Features After Login
**Data Reports:** Users can review reports detected by the app. 

**All Data:** Users can manually verify the data, if the system misses an issue, users can provide feedback directly to improve the system's accuracy over time.

**Devices:** View a list of all devices integrated into the system. 

**Patients:** Explore patient records managed by the system.

**Feedback:** View all feedback submitted by users.

## Author
- [Agni Ramadani](https://github.com/agniramadani)
