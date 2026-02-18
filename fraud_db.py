from fraud_system.db_connect import conn

def insert_image(path):
    cursor = conn.cursor()
    query = "INSERT INTO fraud_images (image_path) VALUES (%s)"
    cursor.execute(query, (path,))
    conn.commit()
    cursor.close()


def fetch_all_images():
    cursor = conn.cursor()
    query = "SELECT image_path FROM fraud_images"
    cursor.execute(query)
    results = cursor.fetchall()
    cursor.close()
    return [row[0] for row in results]
