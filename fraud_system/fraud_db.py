from fraud_system.db_connect import conn

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
    cursor = conn.cursor()
    query = "INSERT INTO fraud_images (image_path) VALUES (?)"
    cursor.execute(query, (path,))
    conn.commit()
    cursor.close()
    print("image inserting:", path)


def fetch_all_images():
    cursor = conn.cursor()
    query = "SELECT image_path FROM fraud_images"
    cursor.execute(query)
    results = cursor.fetchall()
    cursor.close()
    return [row[0] for row in results]
