import sys
from app.core.config import settings
from app.core.database import engine
from app.core.redis import verify_redis_connection
from app.core.security import get_password_hash, verify_password, create_access_token

def test_core():
    print("=== TESTING CORE SETTINGS ===")
    print(f"Project Name: {settings.PROJECT_NAME}")
    print(f"Database URI: {settings.sqlalchemy_database_uri}")
    
    print("\n=== TESTING SECURITY FUNCTIONS ===")
    password = "MySuperSecretPassword123"
    hashed = get_password_hash(password)
    print(f"Plain Password: {password}")
    print(f"Hashed Password: {hashed}")
    
    verified = verify_password(password, hashed)
    print(f"Password Verification: {'SUCCESS' if verified else 'FAILED'}")
    assert verified is True
    
    token = create_access_token(subject="test-user-id")
    print(f"Generated JWT Token: {token}")
    print("Token Generation: SUCCESS")

    print("\n=== TESTING DATABASE CONNECTIVITY ===")
    try:
        connection = engine.connect()
        print("Database Connection: SUCCESS")
        connection.close()
    except Exception as e:
        print(f"Database Connection: FAILED (This is expected if your local Postgres is not yet running. Detail: {e})")

    print("\n=== TESTING REDIS CONNECTIVITY ===")
    redis_ok = verify_redis_connection()
    if redis_ok:
        print("Redis Connection: SUCCESS")
    else:
        print("Redis Connection: FAILED (This is expected if your local Redis cache is not yet running.)")

if __name__ == "__main__":
    test_core()
