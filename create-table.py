import psycopg2

conn = psycopg2.connect("dbname=dq user=dq")
cur = conn.cursor()

cur.execute("""
    CREATE TABLE users (
        id integer CONSTRAINT userskey PRIMARY KEY,
        email text,
        email text, 
        address text
    )
""")
conn.commit()

conn.close()
