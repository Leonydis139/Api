from fastapi import FastAPI, Request
from pydantic import BaseModel
from typing import List, Dict, Optional
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="QuantumRequest API Prototype")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://api-wine-nu-87.vercel.app/"],  # You can replace "*" with your actual frontend URL for security
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app = FastAPI(title="QuantumRequest API Prototype")

# ✅ Models
class QuantumRequest(BaseModel):
    intent: str
    userId: int
    cacheKeys: Optional[List[str]] = []
    requestedComponents: List[str]

class ComponentPayload(BaseModel):
    profile: Optional[Dict] = None
    permissions: Optional[Dict] = None
    notifications: Optional[Dict] = None

class QuantumResponse(BaseModel):
    components: ComponentPayload
    microFunctions: Dict[str, str]
    nextIntents: List[str]

# ✅ Mock Data
mock_user_profile = {
    "name": "Juan Greyling",
    "email": "juanlouw.greyling@gmail.com",
    "lastLogin": "2025-07-04T12:00:00Z"
}

mock_user_permissions = {
    "roles": ["admin", "editor"]
}

mock_user_notifications = {
    "messages": ["Welcome back!", "You have 3 new alerts."]
}

micro_functions = {
    "formatDate": "function(date) { return new Date(date).toLocaleDateString(); }"
}

# ✅ Component Fetcher
def get_component(name: str, cache_keys: List[str]):
    if name == "profile" and "userProfile_v2" not in cache_keys:
        return mock_user_profile
    if name == "permissions" and "userPermissions_v1" not in cache_keys:
        return mock_user_permissions
    if name == "notifications":
        return mock_user_notifications
    return None

# ✅ API Endpoint
@app.post("/quantum")
async def quantum_request(qr: QuantumRequest):
    components = {}

    for comp in qr.requestedComponents:
        data = get_component(comp, qr.cacheKeys)
        if data:
            components[comp] = data

    response = QuantumResponse(
        components=ComponentPayload(**components),
        microFunctions=micro_functions,
        nextIntents=["refreshSession", "loadUserActivity"]
    )

    return response
