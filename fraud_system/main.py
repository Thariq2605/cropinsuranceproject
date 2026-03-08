import os
from fraud_system.fraud_db import insert_image, fetch_all_images
from fraud_system.orb_matcher import orb_match

# Standardize upload directory relative to this file
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
UPLOAD_DIR = os.path.join(BASE_DIR, "uploads")
os.makedirs(UPLOAD_DIR, exist_ok=True)

def check_new_image(new_image_path):
    stored_images = fetch_all_images()

    for old_image in stored_images:

        is_duplicate, matches, ratio = orb_match(new_image_path, old_image)

        print(f"Compared with {old_image}")
        print(f"Good matches: {matches}")
        print(f"Match ratio: {ratio:.2f}")

        if is_duplicate:
            return False, old_image

    return True, None


if __name__ == "__main__":
    # Use relative paths for local testing
    new_image = os.path.join(UPLOAD_DIR, "capture.jpg")

    if not os.path.exists(new_image):
        print(f"Please place an image at {new_image} to test.")
    else:
        valid, matched_image = check_new_image(new_image)
    
        if not valid:
            print("❌ FRAUD DETECTED")
            print("Matched with:", matched_image)
        else:
            print("✅ IMAGE ACCEPTED & STORED")
            insert_image(new_image)
