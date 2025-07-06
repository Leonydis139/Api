from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from libsql_client import create_client
import os
import json

app = FastAPI()

# 🔗 CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Restrict to frontend URL in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 🔑 Environment Variables
API_KEY = os.getenv("QUANTUM_API_KEY")
DB_URL = os.getenv("TURSO_DATABASE_URL")
DB_TOKEN = os.getenv("TURSO_AUTH_TOKEN")

# 🔗 Database Connection
if not DB_URL or not DB_TOKEN:
    raise ValueError("Turso database URL or token is missing in environment variables")

client = create_client(url=DB_URL, auth_token=DB_TOKEN)

# 🚀 Home Route
@app.get("/")
async def read_root():
    return {"status": "QuantumRequest API is live 🚀"}

# 📦 Request Schema
class QuantumRequest(BaseModel):
    intent: str
    userId: int
    cacheKeys: list = []
    requestedComponents: list = []

# 🔑 Quantum Endpoint with DB Save
@app.post("/quantum")
async def quantum_endpoint(request: Request, data: QuantumRequest):
    auth_header = request.headers.get("Authorization")
    if not auth_header or auth_header != f"Bearer {API_KEY}":
        raise HTTPException(status_code=401, detail="Unauthorized")

    # 📝 Insert Request into Database
    await client.execute(
        """
        INSERT INTO quantum_requests (intent, user_id, cache_keys, requested_components)
        VALUES (:intent, :user_id, :cache_keys, :requested_components)
        """,
        {
            "intent": data.intent,
            "user_id": data.userId,
            "cache_keys": json.dumps(data.cacheKeys),
            "requested_components": json.dumps(data.requestedComponents),
        },
    )

    return {
        "message": "Quantum request processed ✅",
        "data": data.dict()
    }

# 📊 Fetch Latest Requests (Optional)
@app.get("/quantum/history")
async def get_request_history():
    result = await client.execute("SELECT * FROM quantum_requests ORDER BY created_at DESC LIMIT 10")
    rows = [dict(row) for row in result.rows]
    return {"history": rows}
