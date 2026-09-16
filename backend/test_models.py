# pyrefly: ignore [missing-import]
from sqlalchemy import create_engine
# pyrefly: ignore [missing-import]
from sqlalchemy.orm import sessionmaker
from app.models import Base, User, ChatSession, Message, ResearchReport, Integration

def test_models():
    print("=== TESTING DATABASE MODELS STRUCTURAL INTEGRITY ===")
    
    # Verify model structure by creating all tables in a transient SQLite in-memory DB
    engine = create_engine("sqlite:///:memory:")
    
    try:
        Base.metadata.create_all(bind=engine)
        print("SQL Alchemy declarative mappings successfully compiled to SQL tables.")
    except Exception as e:
        print(f"Table compilation failed: {e}")
        raise e

    SessionLocal = sessionmaker(bind=engine)
    session = SessionLocal()

    try:
        # 1. Verify User model
        user = User(email="test@domain.com", hashed_password="secure_password_hash")
        session.add(user)
        session.commit()
        print(f"Created User: {user.email} (UUID: {user.id})")

        # 2. Verify ChatSession model
        chat_sess = ChatSession(user_id=user.id, title="Quantum Trends Research")
        session.add(chat_sess)
        session.commit()
        print(f"Created ChatSession: '{chat_sess.title}' (UUID: {chat_sess.id})")

        # 3. Verify Message model
        msg = Message(session_id=chat_sess.id, role="user", content="Research quantum qubits.")
        session.add(msg)
        session.commit()
        print(f"Created Message context: '{msg.content}' (Role: {msg.role})")

        # 4. Verify ResearchReport model
        report = ResearchReport(
            user_id=user.id,
            session_id=chat_sess.id,
            title="Quantum Cryptography Report",
            content="# Details...",
            summary="Dynamic summary abstraction"
        )
        session.add(report)
        session.commit()
        print(f"Created ResearchReport entry: '{report.title}'")

        # 5. Verify Integration model
        integration = Integration(
            user_id=user.id,
            provider="slack",
            credentials={"bot_token": "xoxb-mock-token", "default_channel": "#general"}
        )
        session.add(integration)
        session.commit()
        print(f"Created Integration config: '{integration.provider}'")

        print("\nAll database model schemas validated successfully: SUCCESS")

    except Exception as e:
        print(f"Database insertion test failed: {e}")
        session.rollback()
        raise e
    finally:
        session.close()

if __name__ == "__main__":
    test_models()
