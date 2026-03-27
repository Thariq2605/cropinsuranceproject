import math
import cv2
import numpy as np
from PIL import Image
from PIL.ExifTags import TAGS, GPSTAGS

def is_vegetation_present(image_path, threshold=0.25):
    """
    Check if the image contains enough 'vegetation-like' colors (green/brown).
    Returns True if the percentage of green/brown pixels exceeds the threshold.
    """
    img = cv2.imread(image_path)
    if img is None:
        return False
        
    # Resize for performance
    img = cv2.resize(img, (224, 224))
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    
    # Range for Green (Healthy)
    lower_green = np.array([35, 20, 20])
    upper_green = np.array([85, 255, 255])
    
    # Range for Brown/Dry (Damaged/Dormant)
    lower_brown = np.array([10, 20, 20])
    upper_brown = np.array([35, 255, 255])
    
    mask_green = cv2.inRange(hsv, lower_green, upper_green)
    mask_brown = cv2.inRange(hsv, lower_brown, upper_brown)
    
    combined_mask = cv2.bitwise_or(mask_green, mask_brown)
    vegetation_pixels = cv2.countNonZero(combined_mask)
    total_pixels = img.shape[0] * img.shape[1]
    
    veg_ratio = vegetation_pixels / total_pixels
    print(f"Vegetation Ratio: {veg_ratio:.2f}")
    
    return veg_ratio >= threshold

def get_image_location(image_path):

    image = Image.open(image_path)
    exif_data = image._getexif()

    gps_info = {}

    if exif_data:
        for tag, value in exif_data.items():
            tag_name = TAGS.get(tag)

            if tag_name == "GPSInfo":
                for key in value.keys():
                    gps_info[GPSTAGS.get(key)] = value[key]

    return gps_info
def convert_to_degrees(value):
    try:
        d = float(value[0])
        m = float(value[1])
        s = float(value[2])

        return d + (m / 60.0) + (s / 3600.0)
    except:
        return None    

def calculate_distance(lat1, lon1, lat2, lon2):
    R = 6371  # Earth radius in km

    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)

    a = math.sin(dlat/2)**2 + math.cos(math.radians(lat1)) \
        * math.cos(math.radians(lat2)) * math.sin(dlon/2)**2

    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
    return R * c
