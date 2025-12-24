import mysql.connector

conn = mysql.connector.connect(
    host="localhost",
    user="herbal",
    password="herbalpwd",
    database="herbalglow"
)

cursor = conn.cursor(dictionary=True)
