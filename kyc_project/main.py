from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlmodel import select, Session

from schemas import KYCRequest, KYCValidationResult, DocumentStatus, KYCRecordOut
from validation_engine import validate_all_documents
from db import init_db, get_session
from models_db import KYCRecord
import os


app = FastAPI(
    title="Digital KYC Validation Service",
    version="1.1.0",
    description="Backend service for validating Aadhaar, PAN, and Passport numbers using checksum rules and duplicate detection.",
)
# raw_origins = os.getenv("ALLOWED_ORIGINS", "*")
# allowed_origins = [o.strip() for o in raw_origins.split(",")]

# CORS settings
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"] ,#allowed_origins,  # tighten in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
def on_startup():
    """
    Initialize database on service startup.
    """
    init_db()


@app.get("/health")
def health_check():
    """
    Simple health endpoint to verify service is running.
    """
    return {"status": "ok", "service": "kyc-validation", "version": app.version}


@app.post("/kyc/validate", response_model=KYCValidationResult)
def validate_kyc(payload: KYCRequest):
    """
    Pure validation: Aadhaar, PAN, Passport checksum & format.
    Does NOT store anything in DB.
    """
    overall_ok, raw_results = validate_all_documents(
        aadhaar=payload.aadhaar,
        pan=payload.pan,
        passport=payload.passport,
    )

    document_statuses = [
        DocumentStatus(
            document_type=r.document_type,
            value=r.value,
            is_valid=r.is_valid,
            reason=r.reason,
        )
        for r in raw_results
    ]

    overall_status = "approved" if overall_ok else "rejected"

    return KYCValidationResult(
        success=True,
        overall_status=overall_status,
        documents=document_statuses,
    )


@app.post("/kyc/submit", response_model=KYCValidationResult)
def submit_kyc(payload: KYCRequest, session: Session = Depends(get_session)):
    """
    Full KYC flow: validate documents + check duplicates + store record if approved.

    - Step 1: checksum/format validation (same as /kyc/validate)
    - Step 2: duplicate check in DB (Aadhaar / PAN / Passport)
    - Step 3: if no duplicates and all valid → persist KYCRecord and approve
    """
    # Step 1: run algorithmic validation
    overall_ok, raw_results = validate_all_documents(
        aadhaar=payload.aadhaar,
        pan=payload.pan,
        passport=payload.passport,
    )

    # Build mutable document statuses
    docs: list[DocumentStatus] = [
        DocumentStatus(
            document_type=r.document_type,
            value=r.value,
            is_valid=r.is_valid,
            reason=r.reason,
        )
        for r in raw_results
    ]

    # If any document invalid by logic, we don't hit DB at all
    if not overall_ok:
        return KYCValidationResult(
            success=True,
            overall_status="rejected",
            documents=docs,
        )

    # Step 2: duplicate detection
    # We mark duplicates as invalid at this stage
    for doc in docs:
        if doc.document_type == "aadhaar" and doc.is_valid and payload.aadhaar:
            existing = session.exec(
                select(KYCRecord).where(KYCRecord.aadhaar == payload.aadhaar)
            ).first()
            if existing:
                doc.is_valid = False
                doc.reason = "Duplicate Aadhaar: already used in an existing KYC record."

        if doc.document_type == "pan" and doc.is_valid and payload.pan:
            existing = session.exec(
                select(KYCRecord).where(KYCRecord.pan == payload.pan)
            ).first()
            if existing:
                doc.is_valid = False
                doc.reason = "Duplicate PAN: already used in an existing KYC record."

        if doc.document_type == "passport" and doc.is_valid and payload.passport:
            existing = session.exec(
                select(KYCRecord).where(KYCRecord.passport == payload.passport)
            ).first()
            if existing:
                doc.is_valid = False
                doc.reason = "Duplicate Passport: already used in an existing KYC record."

    # Recompute overall status after duplicate checks
    all_valid = all(d.is_valid for d in docs)
    overall_status = "approved" if all_valid else "rejected"

    # Step 3: if all documents valid and non-duplicate, persist in DB
    if all_valid:
        record = KYCRecord(
            aadhaar=payload.aadhaar,
            pan=payload.pan,
            passport=payload.passport,
        )
        session.add(record)
        session.commit()
        session.refresh(record)

    return KYCValidationResult(
        success=True,
        overall_status=overall_status,
        documents=docs,
    )

from typing import List

@app.get("/admin/kyc-records", response_model=List[KYCRecordOut])
def list_kyc_records(session: Session = Depends(get_session), limit: int = 50):
    """
    Admin endpoint: list recent KYC records stored in the database.
    Default limit = 50.
    """
    records = session.exec(
        select(KYCRecord).order_by(KYCRecord.created_at.desc()).limit(limit)
    ).all()
    return records
