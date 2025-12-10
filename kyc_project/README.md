# Digital KYC – Document Validation & Duplicate Detection (Backend)

This project implements a **backend service for Digital KYC** using:

- ✅ Checksum-based document validation (Aadhaar, PAN, Passport)
- ✅ Duplicate KYC detection using a database
- ✅ Clean, modular FastAPI architecture
- ✅ Environment-based configuration

## Tech Stack

- **Language:** Python 3
- **Framework:** FastAPI
- **DB Layer:** SQLModel (SQLAlchemy)
- **Database (local):** SQLite (`kyc.db`)
- **Config:** `.env` + python-dotenv
- **API Docs:** Swagger UI (`/docs`)

## Project Structure

```text
kyc_project/
├── main.py              # FastAPI app & routes
├── schemas.py           # Pydantic models (request/response)
├── validation_engine.py # Aadhaar/PAN/Passport validation logic
├── models_db.py         # SQLModel ORM models (KYCRecord)
├── db.py                # DB engine, session, init
├── requirements.txt     # Python dependencies
├── .env                 # Environment configuration (DATABASE_URL)
└── kyc.db               # SQLite DB (auto-created)


# 1. Create and activate virtual env
python3 -m venv venv
source venv/bin/activate

# 2. Install dependencies
pip install -r requirements.txt

# 3. Run the API server
uvicorn main:app --reload
