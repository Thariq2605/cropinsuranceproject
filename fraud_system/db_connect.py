import mysql.connector

conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="thariq_2605",
    database="cropinsurance"
)

print("✅ Connected successfully")
