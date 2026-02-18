import os
from fraud_system.fraud_db import insert_image, fetch_all_images
from fraud_system.orb_matcher import orb_match

UPLOAD_DIR = r"c:\Users\moham\Downloads\ricecrop2.jpeg"

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

    new_image = r"c:\Users\moham\Downloads\newricecrop.jpeg"   # Image being uploaded now

    valid, matched_image = check_new_image(new_image)
  
    if not valid:
        print("❌ FRAUD DETECTED")
        print("Matched with:", matched_image)
    else:
        print("✅ IMAGE ACCEPTED & STORED")
        insert_image(new_image)
