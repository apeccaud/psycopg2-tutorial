import csv
import psycopg2

conn = psycopg2.connect("dbname=dq user=dq")
cur = conn.cursor()


# Way 1 : Iterative insertion of rows
with open('user_accounts.csv', 'r') as f:
    next(f)  # Skip first line (header)
    reader = csv.reader(f)
    for row in reader:
        cur.execute("INSERT INTO users VALUES (%s, %s, %s, %s)", row)
conn.commit()
# ------------------------------------


# Way 2 : Multiple insertions (using mogrify)
with open("ign.csv", "r") as f:
    next(f)
    reader = csv.reader(f)
    mogrified = [
        cur.mogrify("(%s, %s, %s, %s, %s, %s, %s, %s, %s)", row).decode("utf-8")
        for row in reader
    ]

cur.execute("INSERT INTO ign_reviews VALUES" + ",".join(mogrified))
conn.commit()
# ------------------------------------


# Way 3 : Copy from python file
# Note : Does not use the CSV module. If a field contains, "," (ex: "Football, Basketball"),
# this code can cause undesired effects
with open('user_accounts.csv', 'r') as f:
    next(f)  # Skip header row
    cur.copy_from(f, 'users', sep=',')
conn.commit()
# ------------------------------------


# Way 4 : Copy from python file with options
# This enables to add options like FORMAT CSV in order to correctly parse CSV files
with open("ign.csv", "r") as f:
    cur.copy_expert("COPY ign_reviews FROM STDIN WITH CSV HEADER", f)
conn.commit()
# ------------------------------------


# Don't forget to close the connection
conn.close()
