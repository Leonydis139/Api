# QuantumRequest Full Project

This project includes:
- **Backend (FastAPI)** with rate limiting, Turso integration, and history pagination.
- **Frontend (React + Vite)** consolidated dashboard with request panel, response panel, and history table.
- **Streamlit App** for quick tests and history display.
- **CI/CD Workflow** for testing, Docker build, and deployments.

## Environment Variables

See `.env.example` for details.

## Structure

```
quantumrequest_full/
├── api/                      # Backend
├── frontend/                 # React frontend
├── streamlit/                # Streamlit app
├── .github/
│   └── workflows/
│       └── build_and_package.yml
├── .env.example
└── README.md
```
