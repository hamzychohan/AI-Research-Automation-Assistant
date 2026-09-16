from pydantic import BaseModel
from datetime import datetime
from uuid import UUID
from typing import Optional

class ResearchReportBase(BaseModel):
    title: str
    content: str
    summary: str
    status: str

class ResearchReportCreate(BaseModel):
    title: str
    content: str
    summary: str
    session_id: Optional[UUID] = None

class ResearchReportResponse(ResearchReportBase):
    id: UUID
    session_id: Optional[UUID] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
