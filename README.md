
---

🚀 QuantumRequest v3 — FastAPI + Turso Cloud

A secure, rate-limited FastAPI microservice for handling Quantum API requests, fully integrated with Turso Cloud (distributed SQLite) for persistent storage and deployed on Vercel or Render.

---

🌐 Live Demo

Your deployed API:
https://api-your-url.vercel.app/
or
https://api-your-url.onrender.com/

---

📦 Tech Stack

FastAPI ⚡

Uvicorn ASGI Server

Pydantic Validation

Turso Cloud (Distributed SQLite) 💾

SlowAPI Rate Limiting

CORS Middleware

Logging & Storage

---

🚀 Features

✅ Secure API Key authentication
✅ Rate limiting (prevent abuse)
✅ Persistent request logs in Turso DB
✅ Fetch recent activity via /logs endpoint
✅ Ready for AI-powered apps, microservices, and frontends

---

📂 Project Structure

quantumrequest/
├── main.py
├── requirements.txt
├── .env.example
└── README.md

---

🔑 Environment Variables (.env)

QUANTUM_API_KEY=sk-quantum-your-secret-key
TURSO_DATABASE_URL=libsql://your-db.turso.io
TURSO_AUTH_TOKEN=your-turso-auth-token

Get these values from Turso Cloud & Vercel Integration.

---

🛠 Installation & Run (Local)

# Clone this repository
git clone https://github.com/your-username/quantumrequest.git
cd quantumrequest

# Install dependencies
pip install -r requirements.txt

# Create .env file and set your keys

# Run locally
uvicorn main:app --reload --port 8000

---

🔗 API Endpoints

Method	Endpoint	Description

GET	/	Health check 🚦
POST	/quantum	Process Quantum request (secured)
GET	/logs	Retrieve recent logs 📜

---

🔒 Security

All /quantum requests must include:


Authorization: Bearer sk-quantum-your-secret-key

Rate limited to 10 requests per minute per IP.

---

💾 Turso Cloud Database

Automatically creates:


CREATE TABLE IF NOT EXISTS quantum_requests (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  user_id INTEGER NOT NULL,
  intent TEXT NOT NULL,
  timestamp TEXT NOT NULL
);

Logs each request with timestamp for later review.

---

🚀 Deployment (Render, Vercel, Railway)

1. Push this project to GitHub.


2. Connect to Render or Vercel.


3. Add environment variables in dashboard.


4. Deploy 🚀

---

📄 License

MIT License.
Made with ❤️ for quantum-inspired apps.


---
