from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from database import get_db_connection, release_db_connection
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust this to your frontend origin
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# User model for request validation
class User(BaseModel):
    username: str
    password: str

@app.on_event("startup")
async def startup_event():
    """Initialize the database."""
    conn = get_db_connection()
    cur = conn.cursor()
    try:
        cur.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id SERIAL PRIMARY KEY,
                username VARCHAR(255) UNIQUE NOT NULL,
                password VARCHAR(255) NOT NULL
            )
        """)
        conn.commit()
    except Exception as e:
        raise RuntimeError(f"Database initialization failed: {str(e)}")
    finally:
        cur.close()
        release_db_connection(conn)

@app.post("/create_user")
async def create_user(user: User):
    """Create a new user."""
    conn = get_db_connection()
    cur = conn.cursor()
    try:
        cur.execute("INSERT INTO users (username, password) VALUES (%s, %s)", (user.username, user.password))
        conn.commit()
        return {"message": "User created successfully!"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    finally:
        cur.close()
        release_db_connection(conn)

@app.post("/login")
async def login(user: User):
    """Authenticate user."""
    conn = get_db_connection()
    cur = conn.cursor()
    try:
        cur.execute("SELECT * FROM users WHERE username = %s AND password = %s", (user.username, user.password))
        result = cur.fetchone()
        if result:
            return {"message": "Login successful!"}
        else:
            raise HTTPException(status_code=401, detail="Invalid credentials")
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    finally:
        cur.close()
        release_db_connection(conn)
