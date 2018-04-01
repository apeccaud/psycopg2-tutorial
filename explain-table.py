import psycopg2
import pprint as pp

conn = psycopg2.connect(dbname="dq", user="hud_admin", password="abc123")
cur = conn.cursor()

# ANALYZE actually RUNS the query
# Without this attribute, EXPLAINS returns an approximation but doesnt actually run the query
cur.execute("""
EXPLAIN (ANALYZE, format json)
SELECT hbc.state, hbc.coc_number, hbc.coc_name, si.name
FROM homeless_by_coc hbc
INNER JOIN state_info si ON si.postal = hbc.state
""")

# Pretty print the EXPLAIN output
pp.pprint(cur.fetchall())