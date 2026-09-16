import redis
import logging
from app.core.config import settings

logger = logging.getLogger(__name__)

# Redis Connection Pool setup
redis_pool = redis.ConnectionPool(
    host=settings.REDIS_HOST,
    port=settings.REDIS_PORT,
    db=0,
    decode_responses=True  # Automatically decodes server responses to strings
)

def get_redis_client() -> redis.Redis:
    """Returns a Redis client instance linked to the application connection pool."""
    return redis.Redis(connection_pool=redis_pool)

def verify_redis_connection() -> bool:
    """Diagnostic check to ping Redis on application boot-up."""
    try:
        client = get_redis_client()
        return client.ping()
    except Exception as e:
        logger.warning(f"Could not connect to Redis: {e}. Session memory caching might be disabled.")
        return False
