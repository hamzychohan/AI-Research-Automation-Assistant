import uuid
# pyrefly: ignore [missing-import]
from sqlalchemy import Column, String, DateTime, ForeignKey, func, Boolean, JSON
# pyrefly: ignore [missing-import]
from sqlalchemy.dialects.postgresql import UUID
# pyrefly: ignore [missing-import]
from sqlalchemy.orm import relationship  
from app.core.database import Base

class Integration(Base):
    __tablename__ = "integrations"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    provider = Column(String, nullable=False)  # 'slack' or 'gmail'
    credentials = Column(JSON, nullable=False)  # Dictionary of credentials (webhooks, token dicts, OAuth profiles)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    
    user = relationship("User", back_populates="integrations")
