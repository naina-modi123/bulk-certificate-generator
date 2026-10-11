from pydantic import BaseModel, EmailStr, Field
from typing import List


class RecipientInput(BaseModel):
    name: str = Field(..., min_length=1)
    email: EmailStr


class CertificateJobRequest(BaseModel):
    recipients: List[RecipientInput] = Field(..., min_length=1)
    course_name: str = Field(..., min_length=1)
    event_date: str = Field(..., min_length=1)