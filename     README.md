# AI Operations Agent

A production-style AI workflow orchestration system built using LangGraph, FastAPI, OpenAI, Streamlit, SQLite, and LangSmith.

This project converts natural language requests into structured execution workflows and performs automated operations such as scheduling meetings and sending emails.

---

# Features

- Natural language task planning using OpenAI
- LangGraph-based workflow orchestration
- Structured task validation
- Retry and failure handling
- Dynamic tool execution
- SQLite persistence layer
- Contact resolution via database
- Email automation using SMTP
- Request audit trail/history
- Execution metrics and timing
- FastAPI backend
- Streamlit frontend
- LangSmith observability and tracing
- Dockerized deployment setup

---

# Architecture

```text
User Input
    ↓
Planner (OpenAI)
    ↓
Validator
    ↓
LangGraph Workflow
    ↓
Tool Execution Layer
    ↓
Database / Email Tools
    ↓
Structured Response
```

---

# Tech Stack

## AI / Agent Frameworks

- OpenAI
- LangGraph
- LangSmith

## Backend

- FastAPI
- SQLAlchemy
- SQLite

## Frontend

- Streamlit

## Deployment

- Docker

---

# Workflow

1. User enters a natural language request
2. Planner converts request into structured JSON
3. Validator filters unsupported tasks
4. LangGraph routes execution
5. Tools execute actions
6. Results, metrics, and execution history are stored

---

# Example Request

```json
{
  "input": "Send email to Akash"
}
```

---

# Example Response

```json
{
  "user_input": "Send email to Akash",
  "plan": {
    "tasks": ["send_email"],
    "entities": {
      "person": "Akash",
      "time": ""
    }
  },
  "results": [
    "Email sent to akash@gmail.com"
  ],
  "status": "success",
  "metrics": {
    "success": 1,
    "failure": 0
  },
  "execution_time_seconds": 4.27
}
```

---

# Project Structure

```text
ai-agent-system/
│
├── agent.py
├── planner.py
├── tools.py
├── models.py
├── logger.py
├── database.py
├── main.py
├── ui.py
├── seed_contacts.py
├── check_history.py
├── requirements.txt
├── Dockerfile
├── .dockerignore
├── logs.txt
├── agent.db
├── .env
└── README.md
```

---

# Setup

## Clone Repository

```bash
git clone <your_repo_url>
cd ai-agent-system
```

---

## Create Virtual Environment

### Mac/Linux

```bash
python -m venv venv
source venv/bin/activate
```

### Windows

```bash
python -m venv venv
venv\Scripts\activate
```

---

## Install Dependencies

```bash
pip install -r requirements.txt
```

---

# Environment Variables

Create a `.env` file:

```env
OPENAI_API_KEY=your_openai_key

EMAIL_USER=your_email@gmail.com
EMAIL_PASS=your_app_password

LANGCHAIN_API_KEY=your_langsmith_key
LANGCHAIN_TRACING_V2=true
LANGCHAIN_PROJECT=ai-operations-agent
```

---

# Run FastAPI Backend

```bash
uvicorn main:app --reload
```

Open Swagger UI:

```text
http://127.0.0.1:8000/docs
```

---

# Run Streamlit UI

```bash
streamlit run ui.py
```

---

# Database Setup

## Seed Contacts

```bash
python seed_contacts.py
```

## Check Request History

```bash
python check_history.py
```

---

# Docker

## Build Docker Image

```bash
docker build -t ai-agent .
```

## Run Docker Container

```bash
docker run -p 8000:8000 --env-file .env ai-agent
```

---

# Current Capabilities

- Schedule meetings
- Send emails
- Store request history
- Store contacts in database
- Track execution metrics
- Track execution latency
- Handle invalid requests safely
- Retry failed executions
- Log workflow execution
- Trace workflows using LangSmith

---

# Key Engineering Concepts Demonstrated

- AI workflow orchestration
- LLM planning systems
- Structured validation
- Retry mechanisms
- Dynamic tool routing
- Persistent audit trails
- Execution observability
- Production-style API design
- Database-driven entity resolution

---

# Future Improvements

- Multi-agent workflows
- PostgreSQL migration
- Async task execution
- Role-based tool permissions
- RAG integration
- Kubernetes deployment

---

# Screenshots To Add

- Streamlit UI
- FastAPI Swagger UI
- LangSmith traces

---

# Author

Dhanush Kumar