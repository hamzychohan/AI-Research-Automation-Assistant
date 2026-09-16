from pydantic import BaseModel
from uuid import UUID
from datetime import datetime
from typing import Dict, Any

class IntegrationBase(BaseModel):
    provider: str  # 'slack' or 'gmail'
    is_active: bool = True

class IntegrationCreate(BaseModel):
    provider: str
    credentials: Dict[str, Any]

class IntegrationResponse(IntegrationBase):
    id: UUID
    credentials: Dict[str, Any]
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
