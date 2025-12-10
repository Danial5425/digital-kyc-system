import os
from sqlmodel import SQLModel, create_engine, Session
from dotenv import load_dotenv

# Load environment variables from .env file if present
load_dotenv()

# Read DB URL from env, fallback to local SQLite
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./kyc.db")

engine = create_engine(DATABASE_URL, echo=False)


def init_db() -> None:
    """
    Create all tables. Call this once at startup.
    """
    from models_db import KYCRecord  # ensure model is imported

    SQLModel.metadata.create_all(engine)


def get_session():
    """
    FastAPI dependency that yields a DB session.
    """
    with Session(engine) as session:
        yield session
