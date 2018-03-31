import psycopg2

conn = psycopg2.connect("dbname=dq user=dq")
cur = conn.cursor()

with open("old_ign_reviews.csv", "w") as f:
    cur.copy_expert('COPY old_ign_reviews TO STDOUT WITH CSV HEADER', f)
