# Yacht MES - Backend API

FastAPI based backend for Aluminum Electric Yacht Manufacturing Execution System.

## Project Structure

```
backend/
├── app/
│   ├── __init__.py
│   ├── main.py              # FastAPI app entry
│   ├── config.py            # Configuration
│   ├── database.py          # Database connection
│   ├── models/              # SQLAlchemy models
│   ├── routers/             # API routes
│   ├── services/            # Business logic
│   ├── schemas/             # Pydantic schemas
│   ├── dependencies/        # FastAPI dependencies
│   └── utils/               # Utilities
├── alembic/                 # Database migrations
├── tests/                   # Test files
├── requirements.txt
├── Dockerfile
└── README.md
```

## Quick Start

```bash
# Install dependencies
pip install -r requirements.txt

# Run development server
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# Access API docs
http://localhost:8000/docs
```
