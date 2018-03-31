import psycopg2

conn = psycopg2.connect("dbname=dq user=dq")
cur = conn.cursor()

'''
Starting with a table containing 3 columns (release_day, release_month, release_year),
create a new column (release_date) and store the combination of the 3 other fields
Then, drop the 3 old columns
'''

# Create new column
cur.execute("ALTER TABLE ign_reviews ADD COLUMN release_date DATE")

# Update new field release_date from fields release_day, release_month and release_year
cur.execute("UPDATE ign_reviews SET release_date = to_date(release_day || '-' || release_month || '-' || release_year, 'DD-MM-YYYY')")

# Drop old columns
cur.execute("ALTER TABLE ign_reviews DROP COLUMN release_day")
cur.execute("ALTER TABLE ign_reviews DROP COLUMN release_month")
cur.execute("ALTER TABLE ign_reviews DROP COLUMN release_year")

# Commit the entire transaction
conn.commit()
