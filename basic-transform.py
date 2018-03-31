from datetime import date
import csv
import psycopg2

conn = psycopg2.connect("dbname=dq user=dq")
cur = conn.cursor()


# Way 1 : Using Python
# This approach is great for tables that contain less than a million rows but as the size of the table increases,
# it becomes unlikely that this approach would work. As the table size increases, it requires even more memory and disk
# space to load and store these files.

mogrified_values = []

with open("old_ign_reviews.csv", "r+") as f:
    # COPY old table to CSV file
    cur.copy_expert("COPY old_ign_reviews TO STDOUT WITH CSV HEADER", f)
    # Set the file's current position to the beginning of the file
    f.seek(0)
    # Skip header
    next(f)
    # Parse file in CSV
    reader = csv.reader(f)
    for row in reader:
        # Transform row
        updated_row = row[:8]
        updated_row.append(date(int(row[8]), int(row[9]), int(row[10])))
        # Mogrify updated row
        mogrified = cur.mogrify("(%s, %s, %s, %s, %s, %s, %s, %s, %s)", updated_row).decode("utf-8")
        mogrified_values.append(mogrified)

# Insert all the updated rows into the new table in one command
cur.execute("INSERT INTO ign_reviews VALUES" + ",".join(mogrified_values))
conn.commit()


# Way 2 : Using SQL
# By running the INSERT command using SELECT, all the processing is done on the Postgres server side which does not
# require us to store in-memory data on the client side. For easy transformations that can be done within SQL, this is
# the best approach to take.

cur.execute("""
INSERT INTO ign_reviews (
    id, score_phrase, title, url, platform, score, genre, editors_choice, release_date
)
SELECT id, score_phrase, title_of_game_review, url, platform, score, genre, editors_choice, 
  to_date(release_day || '-' || release_month || '-' || release_year, 'DD-MM-YYYY') as release_date
FROM old_ign_reviews
""")
conn.commit()
