# Crop Insurance AI platform

## Overview
This is an AI-powered crop insurance claim evaluation platform. It streamlines the process of inspecting crop damage, identifying the type of crop, estimating the percentage of damage/loss, and verifying the claim against potential fraud attempts. 

The application uses an HTML/JS frontend to capture images and device geolocation, and a Python FastAPI backend to run machine learning predictions and interact with a SQLite database.

## Project Structure
```text
cropinsuranceproject/
├── fraud_system/           # Backend API and Machine Learning Modules
│   ├── api.py              # Main FastAPI application and routing
│   ├── pipeline.py         # Business logic pipeline (fraud check, model inference, DB logging)
│   ├── predictoncode.py    # TensorFlow inference logic (identifying the crop type using MobileNet)
│   ├── db_connect.py       # SQLite database connectivity logic
│   ├── fraud_db.py         # Database query logic (image insertions, validation)
│   └── crop_insurance.db   # SQLite database instances for application state
├── index.html              # Frontend user interface
├── script.js               # Frontend webcam capture and API fetching logic
├── requirements.txt        # Python dependency lists
└── dataset/                # Testing images for various crop conditions 
```

## Setup & Running Instructions

### 1. Prerequisites
Ensure you have Python 3 installed. You may also want to use the included virtual environment (`venv`).
If you need to install the dependencies from scratch:
```bash
pip install -r requirements.txt
```

### 2. Start the Backend Server
The backend requires `uvicorn` to run the FastAPI application. Navigate to the root directory of the project and run:

```bash
# If using the provided virtual environment on Linux/Mac:
source venv/bin/activate
uvicorn fraud_system.api:app --reload

# If running directly inside a standard Python environment:
python3 -m uvicorn fraud_system.api:app --reload
```
You should see the message `✅ Connected successfully to SQLite`, indicating the backend is running properly on `http://127.0.0.1:8000`.

### 3. Open the Frontend Application
Simply open `index.html` in your favorite web browser.
- The browser will ask for Camera and Location permissions. Accept them.
- Click **Capture & Analyze**, which will snapshot your video feed and send the location data to the backend.
- The web page will display the crop type, percentage of damage, estimated loss, NDVI values, and pinpoint the coordinates on an interactive OSM map.