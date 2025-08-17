# Indian Banks REST API

A FastAPI service that provides REST endpoints for Indian bank and branch data.

**GitHub Repository**: [https://github.com/jainyash0614/indian-banks-api.git](https://github.com/jainyash0614/indian-banks-api.git)

## What This Does

- Lists all banks with optional search
- Gets branch details by IFSC code
- Lists branches for a specific bank with filtering
- Automatically loads CSV data on first run

## Quick Start

```bash
# Setup
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

# Run
uvicorn app.main:app --reload
```

Visit http://127.0.0.1:8000/docs for interactive API docs.

## API Endpoints

- `GET /banks` - List all banks
- `GET /banks?q=STATE` - Search banks by name
- `GET /branches/{ifsc}` - Get branch by IFSC
- `GET /banks/{id}/branches` - Get branches for a bank
- `GET /healthz` - Health check

## Testing

```bash
SKIP_STARTUP=1 pytest -q
```

## Deploy to Render

1. Push your code to GitHub (already done)
2. Go to [Render.com](https://render.com) and create account
3. Create new Web Service
4. Connect to your GitHub repository: `jainyash0614/indian-banks-api`
5. Set build command: `pip install -r requirements.txt`
6. Set start command: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
7. Add environment variable: `SKIP_STARTUP=1`
8. Deploy!

## Project Structure

```
app/
├── main.py      # FastAPI app and endpoints
├── models.py    # SQLAlchemy models
├── schemas.py   # Pydantic response models
├── db.py        # Database connection
└── ingest.py    # CSV data loader
```

## Tech Stack

- FastAPI
- SQLAlchemy 2.0
- SQLite (local) / Render's built-in database
- Pytest for testing

## Time Taken

2 days total development time.
