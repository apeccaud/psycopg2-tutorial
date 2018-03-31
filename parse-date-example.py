import csv
from datetime import date
import psycopg2

conn = psycopg2.connect("dbname=dq user=dq")
cur = conn.cursor()

cur.execute("""
    CREATE TABLE ign_reviews (
        id BIGINT PRIMARY KEY,
        score_phrase VARCHAR(11),
        title TEXT,
        url TEXT,
        platform VARCHAR(20),
        score DECIMAL(3, 1),
        genre TEXT,
        editors_choice BOOLEAN,
        release_date DATE
   )
""")

with open('ign.csv', 'r') as f:
    next(f)
    reader = csv.reader(f)
    for row in reader:
        updated_row = row[:8]
        updated_row.append(date(int(row[8]), int(row[9]), int(row[10])))
        cur.execute("INSERT INTO ign_reviews VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)", updated_row)
conn.commit()
