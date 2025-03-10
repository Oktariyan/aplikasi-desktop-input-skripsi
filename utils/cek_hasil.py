import sqlite3

conn = sqlite3.connect("arsip.db")
cursor = conn.cursor()

cursor.execute("SELECT * FROM arsip")
data = cursor.fetchall()

conn.close()

print(data)  # Harusnya muncul data yang tadi ditambahkan
