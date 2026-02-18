from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from fastapi import FastAPI, File, UploadFile
import shutil
import os

from fraud_system.pipeline import run_pipeline

app = FastAPI(title="Crop Insurance AI API")

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)


@app.get("/")
def home():
    return {"message": "Crop Insurance AI API is running"}

@app.post("/analyze")
async def analyze_crop(file: UploadFile = File(...)):
    file_path = os.path.join(UPLOAD_DIR, file.filename)

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    result = run_pipeline(file_path)
    safe_result = jsonable_encoder(result)
    return JSONResponse(content=safe_result)
