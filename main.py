
from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import os
import logging

# Initialize logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("QuantumRequestAPI")

app = FastAPI(
    title="QuantumRequest API",
    description="A simple secured QuantumRequest API",
    version="2.0.0",
)

# CORS Middleware (✅ Restrict origins in production)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 👉 Change to ["https://your-frontend-domain.com"] in production
    allow_credentials=True,
    allow_methods=["POST", "GET", "OPTIONS"],
    allow_headers=["*"],
)

# Load API Key from Environment Variable (✅ with fail-safe)
API_KEY = os.getenv("QUANTUM_API_KEY")
if not API_KEY:
    logger.error("❌ QUANTUM_API_KEY not found in environment variables!")
    raise RuntimeError("Missing QUANTUM_API_KEY environment variable.")

# Home route (✅ Improved message)
@app.get("/")
async def read_root():
    return {
        "status": "✅ QuantumRequest API is live",
        "version": "2.0.0",
        "documentation": "/docs"
    }

# Request schema
class QuantumRequest(BaseModel):
    intent: str
    userId: int
    cacheKeys: list
    requestedComponents: list

# Secure Quantum Endpoint
@app.post("/quantum")
async def quantum_endpoint(request: Request, data: QuantumRequest):
    auth_header = request.headers.get("Authorization")
    expected_token = f"Bearer {API_KEY}"

    if not auth_header:
        logger.warning("🚨 Missing Authorization header.")
        raise HTTPException(status_code=401, detail="Missing Authorization header")

    if auth_header != expected_token:
        logger.warning("🚨 Invalid API Key provided.")
        raise HTTPException(status_code=401, detail="Unauthorized access")

    logger.info(f"✅ Quantum request received: intent={data.intent}, userId={data.userId}")

    response = {
        "message": "✅ Quantum request processed successfully",
        "request": data.dict(),
    }

    return response
