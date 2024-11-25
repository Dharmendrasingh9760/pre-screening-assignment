from databases import Database

DATABASE_URL = "postgresql://admin:admin9760@localhost:5432/db-1"

# Async database instance
database = Database(DATABASE_URL)
