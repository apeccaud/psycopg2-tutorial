import psycopg2
from psycopg2.extensions import AsIs

conn = psycopg2.connect(dbname="dq", user="hud_admin", password="eRqg123EEkl")
cur = conn.cursor()

cur.execute("SELECT table_name FROM information_schema.tables WHERE table_schema='public'")
for table in cur.fetchall():
    statement = cur.mogrify("SELECT * FROM %s LIMIT 0", [AsIs(table[0])])
    cur.execute(statement)
    print(cur.description)
    print(" ")
