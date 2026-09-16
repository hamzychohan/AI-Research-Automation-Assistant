from app.schemas.auth import UserCreate, UserResponse
from app.schemas.chat import MessageCreate, ChatSessionCreate
from app.schemas.report import ResearchReportCreate
from app.schemas.integration import IntegrationCreate
# pyrefly: ignore [missing-import]
from pydantic import ValidationError

def test_schemas():
    print("=== TESTING PYDANTIC SCHEMAS VALIDATION ===")

    # 1. Test User validation
    try:
        user_in = UserCreate(email="valid@domain.com", password="securepassword")
        print(f"UserCreate (Valid Input): PASSED (Email: {user_in.email})")
    except ValidationError as e:
        print(f"UserCreate (Valid Input): FAILED (Unexpected: {e})")
        raise e

    try:
        UserCreate(email="invalid_email_format", password="123")
        print("UserCreate (Invalid Email): FAILED (Should have raised validation error)")
        raise AssertionError("Validation did not catch bad email format")
    except ValidationError:
        print("UserCreate (Invalid Email): PASSED (Caught bad format correctly)")

    # 2. Test Chat Session validation
    try:
        sess_in = ChatSessionCreate(title="Quantum AI Research")
        print(f"ChatSessionCreate (Valid Title): PASSED (Title: {sess_in.title})")
        
        # Test defaults
        sess_default = ChatSessionCreate()
        print(f"ChatSessionCreate (Default Title): PASSED (Default: {sess_default.title})")
    except ValidationError as e:
        print(f"ChatSessionCreate: FAILED ({e})")
        raise e

    # 3. Test Message validation
    try:
        msg_in = MessageCreate(role="assistant", content="Hello, human!")
        print(f"MessageCreate (Valid Message): PASSED (Role: {msg_in.role})")
    except ValidationError as e:
        print(f"MessageCreate: FAILED ({e})")
        raise e

    # 4. Test Report validation
    try:
        report_in = ResearchReportCreate(title="Research paper summary", content="# Markdown", summary="TL;DR Abstract")
        print(f"ResearchReportCreate (Valid Report): PASSED (Title: {report_in.title})")
    except ValidationError as e:
        print(f"ResearchReportCreate: FAILED ({e})")
        raise e

    # 5. Test Integration validation
    try:
        integration_in = IntegrationCreate(provider="gmail", credentials={"client_id": "google-id"})
        print(f"IntegrationCreate (Valid Integration): PASSED (Provider: {integration_in.provider})")
    except ValidationError as e:
        print(f"IntegrationCreate: FAILED ({e})")
        raise e

    print("\nAll Pydantic schema validation tests completed successfully: SUCCESS")

if __name__ == "__main__":
    test_schemas()
