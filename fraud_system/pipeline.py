from fraud_system.main import check_new_image
from fraud_system.predictoncode import predict_crop
from fraud_system.damageanalysis import crop_damage_analysis
from fraud_system.lossestimation import crop_loss_estimation
from fraud_system.fraud_db import insert_image
from fraud_system.utils import is_vegetation_present
import os

print("PIPELINE FILE LOADED")

def run_pipeline(new_image_path):
    # Step 1: Duplicate/Fraud detection
    # We check this first to identify if the exact image was used before
    is_valid, matched_image = check_new_image(new_image_path)
    if not is_valid:
        # Extract filename from path for cleaner response
        matched_filename = os.path.basename(matched_image)
        return {
            "status": "Rejected",
            "reason": f"Fraud detected (duplicate image)",
            "matched_with": matched_filename
        }

    # Step 2: Basic Vegetation Check (Color/Texture)
    # To quickly filter out non-crop images like cars or furniture
    if not is_vegetation_present(new_image_path, threshold=0.25):
        return {
            "status": "Rejected",
            "reason": "Not a crop field (No significant vegetation detected)"
        }

    # Step 3: AI Crop type identification
    crop, confidence = predict_crop(new_image_path)

    # Increased threshold for better accuracy
    if confidence < 80:
        return {
            "status": "Rejected",
            "reason": f"Not a crop field (Low confidence: {confidence:.1f}%)",
            "crop_type": str(crop),
            "confidence": float(round(confidence, 2))
        }

    # Step 4: Crop damage analysis
    damage = crop_damage_analysis(new_image_path)

    # Step 5: Crop loss estimation
    loss = crop_loss_estimation(damage)

    # Final Decision Logic
    if damage < 5:
        status = "No Significant Damage"
    else:
        status = "Eligible for Claim"

    # If eligible, we store it in the database for future duplicate checks
    if status == "Eligible for Claim":
        insert_image(new_image_path)

    return {
        "status": status,
        "crop_type": str(crop),
        "confidence": float(round(confidence, 2)),
        "damage_percentage": float(damage),
        "loss_percentage": float(loss)
    }
