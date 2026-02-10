# Backend - FastAPI Dashboard API

This is a FastAPI-based backend for the Dashboard application, implemented using an MVC (Model-View-Controller) architecture.

## Tech Stack
- **FastAPI**: Web framework
- **SQLAlchemy**: ORM
- **SQLite**: Database (Local)
- **Pydantic**: Data validation

## Project Structure
```
backend/
├── app/
│   ├── main.py            # Entry point
│   ├── database.py        # Database configuration
│   ├── models/            # SQLAlchemy Database Models (Model)
│   ├── schemas/           # Pydantic Schemas (Validation)
│   └── controllers/       # API Routers (Controller)
├── seed_db.py             # Script to populate database from Sheets
└── requirements.txt       # Dependencies
```

## Setup Instructions

1. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Seed the Database**:
   Populate your local `sql_app.db` with data from the current Google Sheet:
   ```bash
   python seed_db.py
   ```

3. **Run the Server**:
   ```bash
   uvicorn app.main:app --reload
   ```

The API will be available at `http://127.0.0.1:8000`. You can view the interactive documentation at `http://127.0.0.1:8000/docs`.

## Integration with Frontend
To connect the frontend to this new backend, update `frontend/src/services/api.js` to point to `http://localhost:8000` instead of the Google Sheets URL.

# backend
