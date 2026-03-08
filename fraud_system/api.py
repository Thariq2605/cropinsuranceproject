from fastapi import FastAPI, File, UploadFile, Form
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse, HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import shutil
import os

from fraud_system.fraud_db import get_land_coordinates
from fraud_system.utils import calculate_distance, get_image_location, convert_to_degrees
from fraud_system.satellite_service import get_ndvi, get_ndvi_heatmap


print("API FILE LOADED")

from fraud_system.pipeline import run_pipeline
print(run_pipeline)

from fastapi.staticfiles import StaticFiles

app = FastAPI(title="crop Insurance AI API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    )

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
UPLOAD_DIR = os.path.join(BASE_DIR, "uploads")
os.makedirs(UPLOAD_DIR, exist_ok=True)

# Define static directory
ROOT_DIR = os.path.dirname(BASE_DIR)

@app.get("/satellite-analysis")
def satellite_analysis(lat: float, lon: float):

    ndvi = get_ndvi(lat, lon)

    return {
        "location": [lat, lon],
        "ndvi_value": ndvi
    }

@app.post("/verify_land_location")
def verify_land_location(
    farmer_id: str,
    survey_number: str,
    latitude: float,
    longitude: float
):

    registered_lat, registered_lon = get_land_coordinates(farmer_id, survey_number)

    if registered_lat is None:
        return {"status": "Invalid Farmer or Survey Number"}

    distance = calculate_distance(
        latitude, longitude,
        registered_lat, registered_lon
    )

    if distance > 0.5:
        return {"status": "Location Mismatch - Access Denied"}

    return {"status": "Verification Successful"}
    

@app.post("/analyze")
async def analyze_crop(
    file: UploadFile = File(...),
    latitude: float = Form(None),
    longitude: float = Form(None)
):
    file_path = os.path.join(UPLOAD_DIR, file.filename)

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # Use coordinates from form if provided, else fall back to EXIF (though unlikely from web capture)
    lat = latitude
    lon = longitude

    if lat is None or lon is None:
        gps_data = get_image_location(file_path)
        if "GPSLatitude" in gps_data and "GPSLongitude" in gps_data:
            lat = convert_to_degrees(gps_data["GPSLatitude"])
            lon = convert_to_degrees(gps_data["GPSLongitude"])

    # Run satellite NDVI
    ndvi = None
    if lat is not None and lon is not None:
        try:
            ndvi = get_ndvi(lat, lon)   
        except Exception as e:
            print(f"NDVI calculation error: {e}")

    result = run_pipeline(file_path)
        
    result["latitude"] = lat
    result["longitude"] = lon
    result["ndvi"] = ndvi

    heatmap = None
    if lat and lon:
        try:
            heatmap = get_ndvi_heatmap(lat, lon)
        except Exception as e:
            print(f"Heatmap generation error: {e}")
            
    result["ndvi_heatmap"] = heatmap

    map_url = None
    if lat and lon:
        map_url = f"https://www.openstreetmap.org/?mlat={lat}&mlon={lon}#map=15/{lat}/{lon}"
    result["map_url"] = map_url


    safe_result = jsonable_encoder(result)
    return JSONResponse(content=safe_result)

# Mount all frontend files at the root level so index.html, map.html, and script.js work seamlessly
app.mount("/", StaticFiles(directory=ROOT_DIR, html=True), name="frontend")
