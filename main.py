from fastapi import FastAPI, Request, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from libsql_client import create_client
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
import os
import json

# Initialize FastAPI app
app = FastAPI()

# Rate Limiter Setup
limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# CORS Configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load Environment Variables
API_KEY = os.getenv("QUANTUM_API_KEY")
DB_URL = os.getenv("TURSO_DATABASE_URL")
DB_TOKEN = os.getenv("TURSO_AUTH_TOKEN")

if not all([API_KEY, DB_URL, DB_TOKEN]):
    raise RuntimeError("❌ Missing required environment variables.")

# Database Client
client = create_client(url=DB_URL, auth_token=DB_TOKEN)

# Request Model
class QuantumRequest(BaseModel):
    intent: str
    userId: int
    cacheKeys: list[str] = []
    requestedComponents: list[str] = []

# API Key Verification
async def verify_api_key(request: Request):
    auth_header = request.headers.get("Authorization")
    if not auth_header or not auth_header.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Missing authorization header.")
    
    token = auth_header.split(" ")[1]
    if token != API_KEY:
        raise HTTPException(status_code=401, detail="Invalid API key.")
    return True

# Health Check
@app.get("/")
async def health_check():
    return {"status": "active", "service": "QuantumRequest API"}

# Quantum Request Endpoint
@app.post("/quantum")
@limiter.limit("10/minute")
async def quantum_endpoint(
    request: Request,  # ✅ Required for limiter
    data: QuantumRequest,
    auth: bool = Depends(verify_api_key)
):
    await client.execute(
        """
        INSERT INTO quantum_requests (intent, user_id, cache_keys, requested_components)
        VALUES (?, ?, ?, ?)
        """,
        [
            data.intent,
            data.userId,
            json.dumps(data.cacheKeys),
            json.dumps(data.requestedComponents),
        ],
    )

    # Get last inserted ID
    result = await client.execute("SELECT last_insert_rowid()")
    request_id = result.rows[0][0]

    return {
        "status": "success",
        "message": "Quantum request processed.",
        "request_id": request_id,
        "components": {comp: f"data_for_{comp}" for comp in data.requestedComponents},
    }

# History Endpoint with Pagination
@app.get("/quantum/history")
@limiter.limit("30/minute")
async def get_history(
    request: Request,  # ✅ Required for limiter
    limit: int = 10,
    offset: int = 0,
    auth: bool = Depends(verify_api_key)
):
    result = await client.execute(
        """
        SELECT * FROM quantum_requests
        ORDER BY created_at DESC
        LIMIT ? OFFSET ?
        """,
        [limit, offset],
    )

    history = [dict(row) for row in result.rows]

    return {
        "count": len(history),
        "history": history,
    }
