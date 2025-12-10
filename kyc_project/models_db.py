from typing import Optional
from datetime import datetime

from sqlmodel import SQLModel, Field, UniqueConstraint


class KYCRecord(SQLModel, table=True):
    """
    Stores one successful KYC record.
    We enforce that Aadhaar, PAN, Passport (if present) are unique.
    """
    __table_args__ = (
        UniqueConstraint("aadhaar", name="uq_kyc_aadhaar"),
        UniqueConstraint("pan", name="uq_kyc_pan"),
        UniqueConstraint("passport", name="uq_kyc_passport"),
    )

    id: Optional[int] = Field(default=None, primary_key=True)

    aadhaar: Optional[str] = Field(default=None, index=True)
    pan: Optional[str] = Field(default=None, index=True)
    passport: Optional[str] = Field(default=None, index=True)

    created_at: datetime = Field(default_factory=datetime.utcnow)
