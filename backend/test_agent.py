import asyncio
import logging
from app.services.agent.agent import run_agent_stream
from app.core.database import SessionLocal

# Configure basic logging to see internal details
logging.basicConfig(level=logging.INFO)

async def test_agent():
    print("=== TESTING LANGCHAIN AGENT STREAMING ===")
    print("Sending Query: 'Search for recent news about OpenAI GPT-5 and send a slack update'\n")

    # Get local database session
    db = SessionLocal()
    
    # Mock identifiers
    import uuid
    user_uuid = uuid.uuid4()
    session_uuid = uuid.uuid4()

    try:
        async for event in run_agent_stream(
            user_input="Search for recent news about OpenAI GPT-5 and send a slack update",
            chat_history=[],
            db=db,
            user_id=user_uuid,
            session_id=session_uuid
        ):
            event_type = event["type"]

            if event_type == "token":
                # Stream raw LLM textual tokens directly to console stdout
                print(event["token"], end="", flush=True)

            elif event_type == "tool_start":
                print(f"\n\n[TOOL STARTED]: Calling tool '{event['tool']}' with input: {event['input']}")

            elif event_type == "tool_end":
                output_str = event["output"]
                truncated_output = output_str[:150] + "..." if len(output_str) > 150 else output_str
                print(f"[TOOL COMPLETED]: Tool '{event['tool']}' returned:\n--- Output ---\n{truncated_output}\n--------------\n")

            elif event_type == "error":
                print(f"\n[AGENT STREAM ERROR]: {event['message']}")

        print("\n\nAgent streaming execution finalized successfully.")

    except Exception as e:
        print(f"\nAgent execution crashed: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    asyncio.run(test_agent())
