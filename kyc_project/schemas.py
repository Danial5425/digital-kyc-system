from typing import Optional, List
from pydantic import BaseModel, Field


class KYCRequest(BaseModel):
    aadhaar: Optional[str] = Field(
        default=None,
        description="12-digit Aadhaar number",
        min_length=10,
        max_length=16,
    )
    pan: Optional[str] = Field(
        default=None,
        description="10-character PAN number",
        min_length=8,
        max_length=12,
    )
    passport: Optional[str] = Field(
        default=None,
        description="8-character Passport number",
        min_length=6,
        max_length=12,
    )


class DocumentStatus(BaseModel):
    """
    Status of each individual document validation.
    """
    document_type: str
    value: str
    is_valid: bool
    reason: Optional[str] = None


class KYCValidationResult(BaseModel):
    """
    Overall KYC validation response.
    """
    success: bool
    overall_status: str  # "approved" or "rejected"
    documents: List[DocumentStatus]

from datetime import datetime

# (keep existing models above: KYCRequest, DocumentStatus, KYCValidationResult)


class KYCRecordOut(BaseModel):
    """
    Response model for stored KYC records (admin view).
    """
    id: int
    aadhaar: str | None = None
    pan: str | None = None
    passport: str | None = None
    created_at: datetime
