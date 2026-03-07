from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from fastapi import FastAPI, File, UploadFile
from fastapi import Form
import shutil
import os
from fastapi import FastAPI
from fraud_system.fraud_db import get_land_coordinates
from fraud_system.utils import calculate_distance
from fastapi import FastAPI
from fraud_system.satellite_service import get_ndvi
from fraud_system.utils import get_image_location
from fraud_system.utils import get_image_location, convert_to_degrees
from fraud_system.satellite_service import get_ndvi_heatmap
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()

print("API FILE LOADED")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    )

from fraud_system.pipeline import run_pipeline
print(run_pipeline)

app = FastAPI(title="crop Insurance AI API")

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
UPLOAD_DIR = os.path.join(BASE_DIR, "uploads")
os.makedirs(UPLOAD_DIR, exist_ok=True)

@app.get("/satellite-analysis")
def satellite_analysis(lat: float, lon: float):

    ndvi = get_ndvi(lat, lon)

    return {
        "location": [lat, lon],
        "ndvi_value": ndvi
    }


@app.get("/")
def home():
    return {"message": "Crop Insurance AI API is running"}

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
    file: UploadFile = File(...)):
    file_path = os.path.join(UPLOAD_DIR, file.filename)

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

# Extract GPS from image
    gps_data = get_image_location(file_path)

    lat = None
    lon = None
    ndvi = None

    if "GPSLatitude" in gps_data and "GPSLongitude" in gps_data:
        lat = convert_to_degrees(gps_data["GPSLatitude"])
        lon = convert_to_degrees(gps_data["GPSLongitude"])

    # Run satellite NDVI
    ndvi = None

    if lat is not None and lon is not None:
        ndvi = get_ndvi(lat, lon)   

    result = run_pipeline(file_path)
        
    result["latitude"] = lat
    result["longitude"] = lon
    result["ndvi"] = ndvi

    heatmap = None
    if lat and lon:
        heatmap = get_ndvi_heatmap(lat, lon)
    result["ndvi_heatmap"] = heatmap

    map_url = None
    if lat and lon:
        map_url = f"https://www.openstreetmap.org/?mlat={lat}&mlon={lon}#map=15/{lat}/{lon}"
    result["map_url"] = map_url

    #result["ndvi_map"] = f"http://127.0.0.1:8000/ndvi-map?lat={lat}&lon={lon}"

    safe_result = jsonable_encoder(result)
    return JSONResponse(content=safe_result)


