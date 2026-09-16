import logging
from typing import AsyncGenerator
from langchain_classic.agents import AgentExecutor, create_tool_calling_agent
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_openai import ChatOpenAI
from langchain_groq import ChatGroq
from app.core.config import settings
from app.services.agent.tools import all_tools
from app.services.agent.prompts import SYSTEM_PROMPT

logger = logging.getLogger(__name__)

def get_agent_executor() -> AgentExecutor:
    """Builds and returns the LangChain AgentExecutor instance."""
    # If Groq is configured, use it as the primary LLM engine
    if settings.GROQ_API_KEY and settings.GROQ_API_KEY != "mock-groq-key-for-setup":
        logger.info(f"Initializing native ChatGroq LLM ({settings.GROQ_MODEL}).")
        llm = ChatGroq(
            groq_api_key=settings.GROQ_API_KEY,
            model=settings.GROQ_MODEL,
            temperature=0.2,
            streaming=True
        )
    else:
        # Ensure api key is present or uses dev mock
        api_key = settings.OPENAI_API_KEY
        if api_key == "mock-openai-key-for-setup":
            # Fall back gracefully so build check passes even with default environment values
            api_key = "sk-placeholder-key-for-dev-only"

        llm = ChatOpenAI(
            openai_api_key=api_key,
            model="gpt-4o-mini",
            temperature=0.2,
            streaming=True
        )

    prompt = ChatPromptTemplate.from_messages([
        ("system", SYSTEM_PROMPT),
        MessagesPlaceholder(variable_name="chat_history"),
        ("human", "{input}"),
        MessagesPlaceholder(variable_name="agent_scratchpad"),
    ])

    agent = create_tool_calling_agent(llm, all_tools, prompt)

    return AgentExecutor(
        agent=agent,
        tools=all_tools,
        verbose=True,
        max_iterations=10,
        handle_parsing_errors=True
    )

async def run_agent_stream(
    user_input: str,
    chat_history: list,
    db,
    user_id,
    session_id
) -> AsyncGenerator[dict, None]:
    """Runs the agent asynchronously, yielding structured events (tokens and tool metrics)

    Yields dictionaries of type:
      - {"type": "token", "token": "abc"}
      - {"type": "tool_start", "tool": "web_search", "input": "..."}
      - {"type": "tool_end", "tool": "web_search", "output": "..."}
    """
    openai_key = settings.OPENAI_API_KEY
    groq_key = settings.GROQ_API_KEY
    is_openai_mock = (openai_key == "mock-openai-key-for-setup" or "placeholder" in openai_key)
    is_groq_mock = (not groq_key or groq_key == "mock-groq-key-for-setup" or "placeholder" in groq_key)

    if is_openai_mock and is_groq_mock:
        import asyncio
        user_input_lower = user_input.lower()
        
        search_output = ""
        if "slack" in user_input_lower:
            yield {
                "type": "tool_start",
                "tool": "send_slack_message",
                "input": {"channel": "#general", "message": f"Summary report on: {user_input}"}
            }
            await asyncio.sleep(1.2)
            yield {
                "type": "tool_end",
                "tool": "send_slack_message",
                "output": "Slack message sent successfully to channel #general."
            }
        elif any(w in user_input_lower for w in ["search", "find", "news", "google", "web"]):
            yield {
                "type": "tool_start",
                "tool": "web_search",
                "input": user_input
            }
            try:
                from app.services.agent.tools.search import web_search
                search_output = web_search(user_input)
            except Exception as e:
                search_output = f"Search failed: {str(e)}"
            yield {
                "type": "tool_end",
                "tool": "web_search",
                "output": search_output
            }
        
        mock_reply = (
            f"🤖 **[Developer Sandbox Mode]**\n\n"
            f"It looks like a valid `OPENAI_API_KEY` has not been set yet (or is the default placeholder key).\n\n"
            f"To resolve this, you can set the `OPENAI_API_KEY` env variable in your `.env` file (or `docker-compose.yml`) and restart the container.\n\n"
            f"Here is a mock response to your query:\n"
            f"> **Query:** {user_input}\n\n"
            f"This is a simulated response demonstrating that the assistant frontend and backend are successfully communicating via WebSockets. "
            f"You can fully test the chat bubble interfaces, tool executing animations, markdown rendering, and user sessions!"
        )
        if search_output:
            mock_reply += f"\n\n### 🔍 Real-Time Tavily Search Results:\n\n{search_output}"
        
        chunk_size = 5
        for i in range(0, len(mock_reply), chunk_size):
            chunk = mock_reply[i:i+chunk_size]
            yield {
                "type": "token",
                "token": chunk
            }
            await asyncio.sleep(0.02)
        return

    executor = get_agent_executor()
    
    # Bundle db session & credentials info into the LangChain configuration context
    config = {
        "configurable": {
            "db": db,
            "user_id": user_id,
            "session_id": session_id
        }
    }

    try:
        async for event in executor.astream_events(
            {"input": user_input, "chat_history": chat_history},
            config=config,
            version="v1"
        ):
            event_type = event["event"]

            if event_type == "on_tool_start":
                yield {
                    "type": "tool_start",
                    "tool": event["name"],
                    "input": event["data"].get("input")
                }

            elif event_type == "on_tool_end":
                # Convert output to string representation
                output_data = event["data"].get("output", "")
                yield {
                    "type": "tool_end",
                    "tool": event["name"],
                    "output": str(output_data)
                }

            elif event_type == "on_chat_model_stream":
                chunk = event["data"].get("chunk")
                if chunk and hasattr(chunk, "content") and chunk.content:
                    yield {
                        "type": "token",
                        "token": chunk.content
                    }

    except Exception as e:
        logger.error(f"Error streaming agent events: {e}")
        yield {
            "type": "error",
            "message": f"Agent error occurred: {str(e)}"
        }
