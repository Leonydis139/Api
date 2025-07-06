from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import os
from libsql_client import create_client

# Initialize FastAPI
app = FastAPI()

# CORS - Replace with your frontend URL for production
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Environment Variables
API_KEY = os.getenv("QUANTUM_API_KEY")
DB_URL = os.getenv("TURSO_DATABASE_URL")
DB_TOKEN = os.getenv("TURSO_AUTH_TOKEN")

# Database Client
client = create_client(url=DB_URL, auth_token=DB_TOKEN)

# Create Table if not exists
client.execute("""
CREATE TABLE IF NOT EXISTS quantum_requests (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    intent TEXT,
    user_id INTEGER,
    cache_keys TEXT,
    requested_components TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
""")

# Pydantic Schema
class QuantumRequest(BaseModel):
    intent: str
    userId: int
    cacheKeys: list
    requestedComponents: list

# Home
@app.get("/")
async def root():
    return {"status": "QuantumRequest API is live 🚀"}

# Process Request and Store
@app.post("/quantum")
async def quantum(request: Request, data: QuantumRequest):
    auth_header = request.headers.get("Authorization")
    if not auth_header or auth_header != f"Bearer {API_KEY}":
        raise HTTPException(status_code=401, detail="Unauthorized")

    # Insert into Database
    client.execute(
        "INSERT INTO quantum_requests (intent, user_id, cache_keys, requested_components) VALUES (?, ?, ?, ?)",
        [
            data.intent,
            data.userId,
            ",".join(data.cacheKeys),
            ",".join(data.requestedComponents)
        ]
    )

    return {"message": "Quantum request processed ✅", "data": data.dict()}

# Retrieve Requests
@app.get("/quantum/history")
async def quantum_history(request: Request):
    auth_header = request.headers.get("Authorization")
    if not auth_header or auth_header != f"Bearer {API_KEY}":
        raise HTTPException(status_code=401, detail="Unauthorized")

    rows = client.execute("SELECT id, intent, user_id, created_at FROM quantum_requests ORDER BY created_at DESC LIMIT 10").rows
    return {"history": rows}
