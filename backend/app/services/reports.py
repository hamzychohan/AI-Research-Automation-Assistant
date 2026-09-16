import uuid
from sqlalchemy.orm import Session
from app.models.report import ResearchReport

def get_reports_by_user(db: Session, user_id: uuid.UUID) -> list:
    """Retrieves all compiled reports belonging to a specific user, sorted by date."""
    return db.query(ResearchReport).filter(
        ResearchReport.user_id == user_id
    ).order_by(ResearchReport.created_at.desc()).all()

def get_report_by_id(db: Session, report_id: uuid.UUID, user_id: uuid.UUID) -> ResearchReport or None:
    """Retrieves a specific report after verifying user ownership."""
    return db.query(ResearchReport).filter(
        ResearchReport.id == report_id, 
        ResearchReport.user_id == user_id
    ).first()
