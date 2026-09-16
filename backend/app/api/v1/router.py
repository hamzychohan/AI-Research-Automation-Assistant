from fastapi import APIRouter
from app.api.v1.endpoints import auth, chat, reports, integrations

api_router = APIRouter()

# Register endpoints under separate resource tags
api_router.include_router(auth.router, prefix="/auth", tags=["Authentication"])
api_router.include_router(chat.router, prefix="/chat", tags=["AI Chat Assistant"])
api_router.include_router(reports.router, prefix="/reports", tags=["Research Reports"])
api_router.include_router(integrations.router, prefix="/integrations", tags=["Integrations Settings"])
