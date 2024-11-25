import psycopg2

conn = psycopg2.connect(
    dbname="db-1",
    user="admin",
    password="admin9760",
    host="localhost",
    port="5432"
)

cur = conn.cursor()

# Execute queries here

cur.close()
conn.close()
