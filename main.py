import os
from fastapi import FastAPI, Header, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Dict, Optional
import openai

# ─── Config ────────────────────────────────────────────────────────────────────
API_KEY = os.getenv("QUANTUM_API_KEY")                # your secret key
OPENAI_KEY = os.getenv("OPENAI_API_KEY")               # for AI next-intents
openai.api_key = OPENAI_KEY

app = FastAPI(title="QuantumRequest API v2")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],     # lock this down to your frontend URL in prod
    allow_methods=["*"],
    allow_headers=["*"],
)

# ─── Models ───────────────────────────────────────────────────────────────────
class QuantumRequest(BaseModel):
    intent: str
    userId: int
    cacheKeys: Optional[List[str]] = []
    requestedComponents: List[str]

class ComponentPayload(BaseModel):
    profile: Optional[Dict] = None
    permissions: Optional[Dict] = None
    notifications: Optional[Dict] = None
    settings: Optional[Dict] = None
    activity: Optional[List[Dict]] = None

class QuantumResponse(BaseModel):
    components: ComponentPayload
    microFunctions: Dict[str, str]
    nextIntents: List[str]

# ─── Mock Data ────────────────────────────────────────────────────────────────
mock_user_profile = {"name": "Juan Greyling", "email": "juan@example.com", "lastLogin": "2025-07-04T12:00:00Z"}
mock_user_permissions = {"roles": ["admin", "editor"]}
mock_user_notifications = {"messages": ["Welcome back!", "You have 3 new alerts."]}
mock_user_settings = {"theme": "dark", "language": "en-ZA"}
mock_user_activity = [
    {"time": "2025-07-05T09:00:00Z", "action": "login"},
    {"time": "2025-07-05T10:15:00Z", "action": "update settings"}
]

# ─── Micro-Functions Library ─────────────────────────────────────────────────
micro_functions = {
    "formatDate": "function(d){return new Date(d).toLocaleDateString();}",
    "formatCurrency": "function(x){return new Intl.NumberFormat().format(x);}",
    "calculateAge": "function(dob){return Math.floor((Date.now()-new Date(dob))/3.154e+10);}"
}

# ─── Helpers ─────────────────────────────────────────────────────────────────
def get_component(name: str, cache_keys: List[str]):
    if name == "profile" and "userProfile_v2" not in cache_keys:
        return mock_user_profile
    if name == "permissions" and "userPermissions_v1" not in cache_keys:
        return mock_user_permissions
    if name == "notifications":
        return mock_user_notifications
    if name == "settings":
        return mock_user_settings
    if name == "activity":
        return mock_user_activity
    return None

def infer_next_intents(state: dict) -> List[str]:
    # a simple OpenAI-powered next-intent suggester
    resp = openai.ChatCompletion.create(
        model="gpt-4o-mini",
        messages=[
            {"role":"system","content":"Suggest 2 next API intents based on this JSON state."},
            {"role":"user","content": str(state)}
        ],
        max_tokens=30
    )
    text = resp.choices[0].message.content.strip()
    return [intent.strip() for intent in text.split(",")][:2]

# ─── Endpoint ────────────────────────────────────────────────────────────────
@app.post("/quantum", response_model=QuantumResponse)
async def quantum_request(
    qr: QuantumRequest,
    x_api_key: str = Header(...),
):
    # 1) API key check
    if API_KEY is None or x_api_key != API_KEY:
        raise HTTPException(401, "Invalid X-API-Key")

    # 2) Gather requested components
    comps = {}
    for comp in qr.requestedComponents:
        data = get_component(comp, qr.cacheKeys)
        if data is not None:
            comps[comp] = data

    # 3) Build response
    resp = {"components": comps, "microFunctions": micro_functions}

    # 4) AI-driven nextIntents
    resp["nextIntents"] = infer_next_intents(resp)

    return resp
