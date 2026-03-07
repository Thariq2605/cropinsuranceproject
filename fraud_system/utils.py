import math
from PIL import Image
from PIL.ExifTags import TAGS, GPSTAGS

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
