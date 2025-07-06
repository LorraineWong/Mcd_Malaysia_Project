import sqlite3

conn = sqlite3.connect("mcd_outlets.db")
cursor = conn.cursor()

# Query for outlets with empty Google Map or Waze link
cursor.execute("""
    SELECT COUNT(*) FROM outlets
    WHERE (google_map_link IS NULL OR google_map_link = '')
       OR (waze_link IS NULL OR waze_link = '')
""")
print("Number of outlets missing Google Map or Waze link:", cursor.fetchone()[0])

results = cursor.fetchall()
for row in results:
    print(row)

conn.close()