# database.py
import psycopg2

def get_db_connection():
    conn = psycopg2.connect(
        dbname="db-1",
        user="admin",
        password="admin9760",
        host="postgres",  # The service name of PostgreSQL in Docker Compose
        port=5432
    )
    return conn

def release_db_connection(conn):
    """Release the database connection by closing it."""
    if conn:
        conn.close()
