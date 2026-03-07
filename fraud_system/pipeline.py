from fraud_system.main import check_new_image
from fraud_system.predictoncode import predict_crop
from fraud_system.damageanalysis import crop_damage_analysis
from fraud_system.lossestimation import crop_loss_estimation
from fraud_system.fraud_db import insert_image
from fraud_system.fraud_db import get_land_coordinates
from fraud_system.utils import calculate_distance

print("PIPELINE FILE LOADED")

def run_pipeline(new_image_path):

    # Step 2: Fraud detection
    is_valid, matched_image = check_new_image(new_image_path)
    if not is_valid:
        return {
        "status": "Rejected",
        "reason": "Fraud detected (duplicate image)"
        }


    # Step 3: Crop type identification
    crop, confidence = predict_crop(new_image_path)

    if confidence < 60:
        return {
            "status" : "Invalid Image - Not crop field"
        }
        


    # Step 3: Crop damage analysis
    damage = crop_damage_analysis(new_image_path)

    # Step 4: Crop loss estimation
    loss = crop_loss_estimation(damage)

    if confidence < 50:
        status = "Invalid Image - Not crop field"

    elif 50 <= confidence < 70:
        status = "Low Confidence - Manual Review"

    elif damage < 5:
        status = "No Significant Damage"

    else:
        status = "Eligible for Claim"

    if status == "Eligible for Claim":
        insert_image(new_image_path)

    # Final result
    return {
        "status": status,
        "crop_type": str(crop),
        "confidence": float(round(confidence, 2)),
        "damage_percentage": float(damage),
        "loss_percentage": float(loss)
    }
