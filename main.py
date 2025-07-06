from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from slowapi import Limiter
from slowapi.util import get_remote_address
from libsql_client import create_client
from dotenv import load_dotenv
import os
import logging
from datetime import datetime

# Load environment variables
load_dotenv()
API_KEY = os.getenv("QUANTUM_API_KEY")
DB_URL = os.getenv("TURSO_DATABASE_URL")
DB_TOKEN = os.getenv("TURSO_AUTH_TOKEN")

# Turso DB client
client = create_client(url=DB_URL, auth_token=DB_TOKEN)

# Create table if not exists
client.execute("""
CREATE TABLE IF NOT EXISTS quantum_requests (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    intent TEXT NOT NULL,
    timestamp TEXT NOT NULL
);
""")

# FastAPI app + Middleware
app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter

# Logging setup
logging.basicConfig(filename="quantum_api.log", level=logging.INFO, format="%(asctime)s - %(message)s")

# Request schema
class QuantumRequest(BaseModel):
    intent: str
    userId: int
    cacheKeys: list
    requestedComponents: list

@app.get("/")
async def home():
    return {"status": "QuantumRequest v3 with Turso 🚀"}

@app.post("/quantum")
@limiter.limit("10/minute")
async def quantum_endpoint(request: Request, data: QuantumRequest):
    auth_header = request.headers.get("Authorization")
    if not auth_header or auth_header != f"Bearer {API_KEY}":
        raise HTTPException(status_code=401, detail="Unauthorized")

    logging.info(f"Received Quantum intent '{data.intent}' from user {data.userId}")
    
    # Save to Turso
    client.execute(
        "INSERT INTO quantum_requests (user_id, intent, timestamp) VALUES (?, ?, ?);",
        [data.userId, data.intent, datetime.utcnow().isoformat()]
    )

    return {"message": "Quantum request processed ✅", "data": data.dict()}

@app.get("/logs")
async def fetch_logs():
    result = client.execute("SELECT * FROM quantum_requests ORDER BY timestamp DESC LIMIT 10;")
    return {"recent_logs": result["rows"]}
