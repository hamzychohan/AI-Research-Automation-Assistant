import logging
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.v1.router import api_router
from app.core.config import settings
from app.core.redis import verify_redis_connection

# Configure standard console logging formats
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s"
)
logger = logging.getLogger(__name__)

app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json"
)

# Setup CORS middleware for local frontend cross-origin requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust to specific domains in production environments
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
def on_startup():
    logger.info("AI Research & Automation Assistant backend initializing...")
    # Diagnostic test for Redis Cache connection
    if verify_redis_connection():
        logger.info("Redis cache successfully pinged.")
    else:
        logger.warning("Redis server offline. Active sessions history caching is unavailable.")

@app.get("/health", tags=["Diagnostics"])
def health_check():
    """Simple status route for container orchestration health checks."""
    return {"status": "healthy", "project": settings.PROJECT_NAME}

# Mount core api endpoints
app.include_router(api_router, prefix=settings.API_V1_STR)
