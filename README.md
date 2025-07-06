
---

🚀 QuantumRequest API

A simple, secure, and lightweight FastAPI-based microservice for handling QuantumRequest data with API key authentication and CORS support.


---

🌐 Live Demo

🔗 https://api-8lyl.onrender.com
🔗 Interactive Docs: https://api-8lyl.onrender.com/docs


---

📦 Features

✅ FastAPI-powered lightweight REST API
✅ Secure token-based access (Bearer Token)
✅ CORS-enabled for frontend integration
✅ Automatic OpenAPI documentation (/docs and /redoc)
✅ Easy deployment to Render, Heroku, or any cloud provider
✅ Fully typed with Pydantic models for validation


---

🚀 Quick Start

1️⃣ Clone the Repository

git clone https://github.com/yourusername/quantumrequest-api.git
cd quantumrequest-api

2️⃣ Install Dependencies

python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

3️⃣ Set Environment Variable

Create a .env file (or set it directly in your environment):

QUANTUM_API_KEY=sk-quantum-93jd8sd82h3shd83h9sd8hs

Or on Linux/Mac:

export QUANTUM_API_KEY=sk-quantum-93jd8sd82h3shd83h9sd8hs


---

4️⃣ Run the Server

uvicorn main:app --reload --host 0.0.0.0 --port 8000

Visit:
📄 Swagger UI: http://localhost:8000/docs
📄 Redoc: http://localhost:8000/redoc


---

🔐 Authentication

All /quantum POST requests require a valid API key passed in the Authorization header:

Authorization: Bearer sk-quantum-93jd8sd82h3shd83h9sd8hs


---

📬 Example Request (with cURL)

curl -X POST https://api-8lyl.onrender.com/quantum \
-H "Content-Type: application/json" \
-H "Authorization: Bearer sk-quantum-93jd8sd82h3shd83h9sd8hs" \
-d '{
  "intent": "loadUserActivity",
  "userId": 123,
  "cacheKeys": ["user_123", "activity"],
  "requestedComponents": ["profile", "notifications"]
}'


---

📄 QuantumRequest Payload Structure

Field	Type	Description

intent	string	The intended action (e.g., refreshSession)
userId	int	Unique identifier for the user
cacheKeys	list	Cache keys related to the request
requestedComponents	list	List of UI components requested



---

⚙ Deployment Guide

✅ Supports Render.com, Heroku, AWS, Azure, etc.
✅ Add QUANTUM_API_KEY as an environment variable in your cloud provider's dashboard.


---

🛡 Security Notes

Never expose your real API key in public repos or frontend code.

Restrict allow_origins in main.py to specific domains in production.

Consider adding rate limiting and logging for production environments.



---

📜 License

MIT License © Juan Greyling


---
