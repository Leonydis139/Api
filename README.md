
---

🌌 QuantumRequest API — FastAPI Microservice 🚀

Secure, scalable, and developer-friendly microservice for handling QuantumRequest operations via FastAPI. Designed for seamless backend/frontend integration with robust authentication and modular request handling.


---

🌐 Live Demo & Documentation

API: https://api-8lyl.onrender.com

Swagger UI: /docs

Redoc UI: /redoc



---

✨ Key Features

✅ FastAPI — Lightning-fast Python API framework
✅ Token-based Authentication — Secure every request
✅ CORS Support — Smooth cross-origin communication
✅ Typed Validation — Strict schema with Pydantic models
✅ Plug & Play Deployment — Works on Render, Heroku, or any cloud
✅ Auto-generated Docs — Built-in OpenAPI/Swagger
✅ Minimal & Modular — Easy to extend and maintain


---

📁 Folder Structure

quantumrequest-api/
├── main.py               # FastAPI application
├── requirements.txt      # Python dependencies
└── README.md             # Project documentation


---

🚀 Quick Start

1️⃣ Clone the Repository

git clone https://github.com/yourusername/quantumrequest-api.git
cd quantumrequest-api

2️⃣ Create Virtual Environment & Install Dependencies

python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

3️⃣ Set Your API Key

✅ Create .env (or set manually):

QUANTUM_API_KEY=sk-quantum-your-real-api-key

Or export in terminal:

export QUANTUM_API_KEY=sk-quantum-your-real-api-key

4️⃣ Start the Development Server

uvicorn main:app --reload --host 0.0.0.0 --port 8000

🔗 Open: http://localhost:8000/docs


---

🔑 Authentication Guide

All POST requests to /quantum must include:

Authorization: Bearer sk-quantum-your-real-api-key

🚨 Without this header → 401 Unauthorized.


---

📦 QuantumRequest JSON Payload

Field	Type	Required	Description

intent	string	✅ Yes	Action intent (refreshSession, etc.)
userId	integer	✅ Yes	Unique user identifier
cacheKeys	list	✅ Yes	List of cache keys
requestedComponents	list	✅ Yes	Components to be returned (profile, etc.)



---

✅ Sample cURL Request:

curl -X POST https://api-8lyl.onrender.com/quantum \
-H "Content-Type: application/json" \
-H "Authorization: Bearer sk-quantum-your-real-api-key" \
-d '{
  "intent": "loadUserActivity",
  "userId": 42,
  "cacheKeys": ["user_42", "activity_log"],
  "requestedComponents": ["profile", "notifications"]
}'


---

🚀 Deployment Tips (Render, Heroku, AWS)

1. Set QUANTUM_API_KEY in the cloud provider’s environment variables.


2. Expose port 0.0.0.0:10000 (or default).


3. Restrict CORS origins in production:

allow_origins=["https://your-frontend.com"]




---

🔐 Security Enhancements (Recommended)

✅ Restrict CORS
✅ Add rate limiting (slowapi or redis-throttle)
✅ Add logging and error tracking (sentry_sdk)
✅ Rotate API keys periodically

---

📜 License

MIT License — Juan Greyling 2025 ©


---
