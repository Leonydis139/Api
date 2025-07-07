from fastapi import FastAPI, Request, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from libsql_client import create_client
import os, json
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded

app = FastAPI()

limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

API_KEY = os.getenv("QUANTUM_API_KEY")
DB_URL = os.getenv("TURSO_DATABASE_URL")
DB_TOKEN = os.getenv("TURSO_AUTH_TOKEN")
if not all([API_KEY, DB_URL, DB_TOKEN]):
    raise RuntimeError("Missing required env vars")

client = create_client(url=DB_URL, auth_token=DB_TOKEN)
client.execute("""
CREATE TABLE IF NOT EXISTS quantum_requests (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  intent TEXT NOT NULL,
  user_id INTEGER NOT NULL,
  cache_keys TEXT,
  requested_components TEXT,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
""")

class QuantumRequest(BaseModel):
    intent: str
    userId: int
    cacheKeys: list[str] = []
    requestedComponents: list[str] = []

async def verify_api_key(request: Request):
    auth = request.headers.get("Authorization","")
    if not auth.startswith("Bearer "):
        raise HTTPException(401, "Missing authorization")
    token = auth.split()[1]
    if token != API_KEY:
        raise HTTPException(401, "Invalid API key")

@app.get("/")
async def health():
    return {"status":"active"}

@app.post("/quantum")
@limiter.limit("10/minute")
async def quantum(req: Request, data: QuantumRequest, ok=Depends(verify_api_key)):
    client.execute(
        "INSERT INTO quantum_requests (intent,user_id,cache_keys,requested_components) VALUES (?,?,?,?)",
        [data.intent, data.userId, json.dumps(data.cacheKeys), json.dumps(data.requestedComponents)]
    )
    rid = client.execute("SELECT last_insert_rowid();").rows[0][0]
    return {
        "status":"success","id":rid,
        "components":{c:f"data_{c}" for c in data.requestedComponents}
    }

@app.get("/quantum/history")
@limiter.limit("30/minute")
async def history(req: Request, limit: int = 10, offset: int = 0, ok=Depends(verify_api_key)):
    res = client.execute(
        "SELECT * FROM quantum_requests ORDER BY created_at DESC LIMIT ? OFFSET ?",
        [limit, offset]
    )
    return {"count":len(res.rows), "history":[dict(r) for r in res.rows]}
