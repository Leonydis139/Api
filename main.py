from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from slowapi import Limiter
from slowapi.util import get_remote_address
from sqlalchemy import create_engine, Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import os
import logging
from datetime import datetime

# Load .env
load_dotenv()
API_KEY = os.getenv("QUANTUM_API_KEY")
DATABASE_URL = os.getenv("DATABASE_URL")

# Logging setup
logging.basicConfig(filename="quantum_api.log", level=logging.INFO, format="%(asctime)s - %(message)s")

# SQLAlchemy setup
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class RequestLog(Base):
    __tablename__ = "request_logs"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, nullable=False)
    intent = Column(String, nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow)

Base.metadata.create_all(bind=engine)

# FastAPI & Middleware
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

# Request Schema
class QuantumRequest(BaseModel):
    intent: str
    userId: int
    cacheKeys: list
    requestedComponents: list

@app.get("/")
async def root():
    return {"status": "QuantumRequest API + PostgreSQL 💾"}

@app.post("/quantum")
@limiter.limit("10/minute")
async def quantum_endpoint(request: Request, data: QuantumRequest):
    auth_header = request.headers.get("Authorization")
    if not auth_header or auth_header != f"Bearer {API_KEY}":
        logging.warning(f"Unauthorized request from {get_remote_address(request)}")
        raise HTTPException(status_code=401, detail="Unauthorized")

    logging.info(f"Quantum request by user {data.userId} - intent: {data.intent}")

    # Save to Postgres
    db = SessionLocal()
    log_entry = RequestLog(user_id=data.userId, intent=data.intent)
    db.add(log_entry)
    db.commit()
    db.close()

    return {"message": "Quantum request processed ✅", "data": data.dict()}

@app.get("/logs")
async def get_logs():
    db = SessionLocal()
    logs = db.query(RequestLog).order_by(RequestLog.timestamp.desc()).limit(10).all()
    db.close()
    return {"recent_requests": [{"id": log.id, "user_id": log.user_id, "intent": log.intent, "timestamp": log.timestamp} for log in logs]}
