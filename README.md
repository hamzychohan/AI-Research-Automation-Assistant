# 🤖 AI Research & Automation Assistant

![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi)
![Next.js](https://img.shields.io/badge/Next.js-000000?style=for-the-badge&logo=nextdotjs&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-316192?style=for-the-badge&logo=postgresql&logoColor=white)
![Redis](https://img.shields.io/badge/Redis-DC382D?style=for-the-badge&logo=redis&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white)
![TypeScript](https://img.shields.io/badge/TypeScript-007ACC?style=for-the-badge&logo=typescript&logoColor=white)
![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)

An end-to-end full-stack autonomous AI agent system designed for conducting deep web research, generating structured technical reports, and performing workflow automations across communication platforms (Slack, Gmail).

---

## 🌟 Key Features

- 🤖 **Autonomous Multi-Tool Agent**: Built on LangChain with support for both **OpenAI (GPT-4o)** and **Groq (Llama-3.1)** LLM backends.
- ⚡ **Real-Time Streaming**: Real-time token streaming and step-by-step tool execution feedback via WebSockets.
- 🔍 **Live Web Search**: Integrates **Tavily API** to gather real-time web content and references for research tasks.
- 📬 **Workflow Automations**:
  - **Slack Integration**: Automatically post research summaries or notifications directly into configured Slack channels.
  - **Gmail Integration**: Draft or send automated email reports via OAuth / API credentials.
- 📊 **Research Report Generator**: Export structured research findings into downloadable PDF or Markdown documents.
- 🔐 **Authentication & Security**: JWT authentication with passlib password hashing and user session management.
- 🗄️ **Persistent & Cached Memory**: PostgreSQL for relational user and chat data; Redis for caching active chat sessions and fast retrieval.
- 🐳 **Containerized Setup**: Fully containerized environment powered by Docker & Docker Compose.

---

## 📐 Architecture Overview

```
                          ┌───────────────────────────┐
                          │   Next.js 14 Frontend     │
                          │ (TypeScript, React, WS)   │
                          └─────────────┬─────────────┘
                                        │ WebSockets / HTTP
                                        ▼
                          ┌───────────────────────────┐
                          │     FastAPI Backend       │
                          │   (LangChain Executor)    │
                          └──────┬──────────┬─────────┘
                                 │          │
                 ┌───────────────┴─┐      ┌─┴───────────────┐
                 │  PostgreSQL 15  │      │     Redis 7     │
                 │  (Relational)   │      │ (Session Cache) │
                 └─────────────────┘      └─────────────────┘
                                 │
         ┌───────────────────────┼───────────────────────┐
         ▼                       ▼                       ▼
 ┌───────────────┐       ┌───────────────┐       ┌───────────────┐
 │ OpenAI / Groq │       │ Tavily Search │       │ Slack / Gmail │
 │  LLM Engine   │       │   API Tool    │       │ Integrations  │
 └───────────────┘       └───────────────┘       └───────────────┘
```

---

## 🛠️ Tech Stack

### **Backend**
- **Framework**: FastAPI (Python 3.11+)
- **Agent Orchestration**: LangChain, LangChain-OpenAI, LangChain-Groq
- **Database ORM**: SQLAlchemy 2.0 with Alembic database migrations
- **Caching**: Redis
- **Database**: PostgreSQL 15

### **Frontend**
- **Framework**: Next.js 14 (App Router)
- **UI & Components**: React 18, Lucide Icons, Marked (Markdown Renderer)
- **Language**: TypeScript

### **Infrastructure & Tools**
- **Containerization**: Docker & Docker Compose
- **Web Search API**: Tavily Search

---

## 🚀 Quick Start Guide

### Prerequisites
- [Docker](https://www.docker.com/) & [Docker Compose](https://docs.docker.com/compose/)
- Alternatively, **Python 3.11+** and **Node.js 18+** for manual setup.

---

### Method 1: Running with Docker Compose (Recommended)

1. **Clone the repository**:
   ```bash
   git clone https://github.com/hamzychohan/AI-Research-Automation-Assistant.git
   cd AI-Research-Automation-Assistant
   ```

2. **Configure Environment Variables**:
   Copy the example environment file:
   ```bash
   cp backend/.env.example .env
   ```
   *Edit `.env` to supply your `OPENAI_API_KEY`, `TAVILY_API_KEY`, or `GROQ_API_KEY`.*

3. **Start All Services**:
   ```bash
   docker-compose -f docker/docker-compose.yml up --build
   ```

4. **Access the Applications**:
   - **Frontend UI**: [http://localhost:3000](http://localhost:3000)
   - **Backend API Docs**: [http://localhost:8000/docs](http://localhost:8000/docs)
   - **Backend Health Check**: [http://localhost:8000/health](http://localhost:8000/health)

---

### Method 2: Manual Local Development

#### 1. Backend Setup

```bash
cd backend

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Configure environment
cp .env.example .env

# Run database migrations
alembic upgrade head

# Start FastAPI dev server
uvicorn app.main:app --reload --port 8000
```

#### 2. Frontend Setup

```bash
cd frontend

# Install dependencies
npm install

# Run Next.js development server
npm run dev
```

---

## 🔑 Environment Variables Reference

| Variable | Description | Default / Example |
| :--- | :--- | :--- |
| `POSTGRES_USER` | PostgreSQL Username | `postgres` |
| `POSTGRES_PASSWORD` | PostgreSQL Password | `postgres` |
| `POSTGRES_DB` | PostgreSQL Database Name | `ai_assistant` |
| `POSTGRES_HOST` | Database Host Address | `localhost` / `postgres-db` |
| `REDIS_HOST` | Redis Server Host | `localhost` / `redis-cache` |
| `OPENAI_API_KEY` | OpenAI API Key for GPT-4o models | `sk-...` |
| `GROQ_API_KEY` | Groq API Key for Llama-3.1 models | `gsk_...` |
| `TAVILY_API_KEY` | Tavily API Key for real-time web search | `tvly-...` |
| `SLACK_BOT_TOKEN` | Slack Bot User OAuth Token | `xoxb-...` |
| `SLACK_CHANNEL` | Default Slack channel for posts | `#general` |

---

## 📡 API Endpoints Overview

| Method | Endpoint | Description |
| :--- | :--- | :--- |
| **POST** | `/api/v1/auth/register` | Register a new user |
| **POST** | `/api/v1/auth/login` | Log in and receive JWT access token |
| **GET** | `/api/v1/chat/sessions` | Fetch user chat sessions |
| **WS** | `/api/v1/chat/ws/{session_id}` | WebSocket stream for AI chat and agent execution |
| **GET** | `/api/v1/reports` | List generated research reports |
| **POST** | `/api/v1/reports/export` | Export research report as PDF/Markdown |
| **GET** | `/api/v1/integrations` | Fetch configured Slack & Gmail integrations |

---

## 🧪 Running Unit Tests

Run test suites for backend components (agent, core, models, schemas):

```bash
cd backend
python -m pytest test_agent.py test_core.py test_models.py test_schemas.py
```

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
