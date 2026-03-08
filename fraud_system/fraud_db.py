from fraud_system.db_connect import conn
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
UPLOAD_DIR = os.path.join(BASE_DIR, "uploads")

def get_land_coordinates(farmer_id, survey_number):
    cursor = conn.cursor()

    query = """
        SELECT latitude, longitude
        FROM farmer_lands
        WHERE farmer_id = ? AND survey_number = ?
    """

    cursor.execute(query, (farmer_id, survey_number))
    result = cursor.fetchone()

    cursor.close()

    if result:
        return result[0], result[1]
    else:
        return None, None

def insert_image(path):
    # Store only the filename to ensure portability
    filename = os.path.basename(path)
    cursor = conn.cursor()
    query = "INSERT INTO fraud_images (image_path) VALUES (?)"
    cursor.execute(query, (filename,))
    conn.commit()
    cursor.close()
    print("image inserting:", filename)


def fetch_all_images():
    cursor = conn.cursor()
    query = "SELECT image_path FROM fraud_images"
    cursor.execute(query)
    results = cursor.fetchall()
    cursor.close()
    
    # Reconstruct the full path dynamically
    full_paths = []
    for row in results:
        stored_path = row[0]
        # If it was stored as an absolute path previously, try to extract just the filename
        filename = os.path.basename(stored_path)
        full_path = os.path.join(UPLOAD_DIR, filename)
        full_paths.append(full_path)
        
    return full_paths
