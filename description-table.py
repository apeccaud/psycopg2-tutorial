import psycopg2
from psycopg2.extensions import AsIs

conn = psycopg2.connect(dbname="", user="hud_admin", password="eRqg123EEkl")
cur = conn.cursor()

# Get table mapping type_code and type_name
cur.execute("SELECT oid, typname FROM pg_catalog.pg_type")
type_mappings = {
    int(oid): typename
    for oid, typename in cur.fetchall()
}

# Get table names
cur.execute("SELECT table_name FROM information_schema.tables WHERE table_schema='public'")
table_names = cur.fetchall()

# Get readable description of the tables
readable_description = {}
for table in table_names:
    statement = cur.mogrify("SELECT * FROM %s LIMIT 0", (AsIs(table), ))
    cur.execute(statement)
    readable_description[table] = {
        "columns": [
            {
                "name": col.name,
                "type": type_mappings[col.type_code],
                "internal_size": col.internal_size
            }
            for col in cur.description
        ]
    }

print(readable_description)
