from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import os

app = FastAPI()

# 🔗 CORS Middleware (Fixes the 405 error)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # For production, restrict to your frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 🔐 Load Quantum API Key from environment variable
API_KEY = os.getenv("QUANTUM_API_KEY")

# 🚀 Optional Home Route (Fixes 404 on `/`)
@app.get("/")
async def read_root():
    return {"status": "QuantumRequest API is live 🚀"}

# 📦 Define QuantumRequest schema
class QuantumRequest(BaseModel):
    intent: str
    userId: int
    cacheKeys: list
    requestedComponents: list

# 🔑 Secure Quantum Endpoint
@app.post("/quantum")
async def quantum_endpoint(request: Request, data: QuantumRequest):
    auth_header = request.headers.get("Authorization")
    if not auth_header or auth_header != f"Bearer {API_KEY}":
        raise HTTPException(status_code=401, detail="Unauthorized")
    
    # You can add logic here to process the request
    return {"message": "Quantum request received successfully", "data": data.dict()}
