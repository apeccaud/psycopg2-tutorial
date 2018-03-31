import psycopg2

conn = psycopg2.connect("dbname=dq user=dq")
cur = conn.cursor()

cur.execute("SELECT * FROM ign_reviews LIMIT 0")
print(cur.description)
