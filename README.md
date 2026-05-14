# AI Operations Agent

An AI-powered workflow orchestration platform built using LangGraph, FastAPI, OpenAI, Streamlit, SQLAlchemy, and LangSmith.

The system converts natural language requests into structured workflows and executes supported operations such as scheduling meetings and sending emails.

This project demonstrates AI workflow orchestration, backend engineering, workflow execution pipelines, observability, execution tracking, database-driven tooling, and production-style API architecture.

---

# Demo Video

> Add demo video link here

```text
Demo Video:
https://your-demo-link-here
```

---

# Live Deployments

## Streamlit Frontend

```text
https://ai-operations-agent-platform-e3w3pzqsr3oqkyff5rny5f.streamlit.app/
```

## FastAPI Backend

```text
https://ai-operations-agent-platform-p4cj.onrender.com
```

---

# Features

## AI Workflow Orchestration

- Natural language task planning using OpenAI
- LangGraph-based workflow orchestration
- Planner → Validator → Executor architecture
- Structured task validation
- Conditional workflow routing
- Retry and failure handling
- Dynamic tool execution

---

## Backend Engineering

- FastAPI backend APIs
- SQLAlchemy ORM integration
- SQLite database integration
- Contact management APIs
- Request history tracking
- Execution metrics tracking
- Structured logging system
- Dynamic supported tasks API

---

## Frontend

- Streamlit-based interactive UI
- Contact management interface
- Workflow execution interface
- Meetings dashboard
- Execution result visualization
- Metrics and execution time display

---

## Observability

- LangSmith tracing integration
- Workflow execution logging
- Request history tracking
- Success/failure monitoring

---

# System Architecture

```text
User
  ↓
Streamlit Frontend
  ↓
FastAPI Backend
  ↓
LangGraph Workflow
  ├── Planner Node (OpenAI)
  ├── Validator Node
  └── Executor Node
          ├── Email Tool
          └── Meeting Scheduler
  ↓
SQLite Database
  ↓
Logs + LangSmith Tracing
```

---

# Workflow Execution

```text
User Request
    ↓
Planner extracts tasks/entities
    ↓
Validator filters unsupported tasks
    ↓
Executor executes tools
    ↓
Results returned to frontend/API
```

---

# Tech Stack

## AI / Agent Frameworks

- OpenAI
- LangGraph
- LangSmith

---

## Backend

- FastAPI
- SQLAlchemy
- SQLite

---

## Frontend

- Streamlit

---

## Utilities

- Python Dotenv
- Requests
- resend Email Automation

---

# Supported Tasks

| Task | Description |
|---|---|
| schedule_meeting | Schedule meetings |
| send_email | Send emails |

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
ai-operations-agent/
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
├── .gitignore
├── logs.txt
├── agent.db
├── .env
├── screenshots/
└── README.md
```

---

# Setup

## Clone Repository

```bash
git clone https://github.com/Dhanush-kumar-reddy/AI-Operations-Agent-Platform
cd ai-operations-agent
```

---

# Create Virtual Environment

## Mac/Linux

```bash
python -m venv venv
source venv/bin/activate
```

---

## Windows

```bash
python -m venv venv
venv\Scripts\activate
```

---

# Install Dependencies

```bash
pip install -r requirements.txt
```

---

# Environment Variables

Create a `.env` file:

```env
OPENAI_API_KEY=your_openai_key

EMAIL_USER=your_email@gmail.com
EMAIL_PASS=your_email_password

LANGCHAIN_API_KEY=your_langsmith_key
LANGCHAIN_TRACING_V2=true
LANGCHAIN_PROJECT=ai-operations-agent

DATABASE_URL=sqlite:///./agent.db
```

---

# Run FastAPI Backend

```bash
uvicorn main:app --reload
```

Swagger UI:

```text
http://127.0.0.1:8000/docs
```

---

# Run Streamlit Frontend

```bash
streamlit run ui.py
```

---

# Database Setup

## Seed Initial Contacts

```bash
python seed_contacts.py
```

---

## Check Request History

```bash
python check_history.py
```

---

# Contact Management

The Streamlit UI supports dynamic contact management.

Users can:

- Add contacts
- View contacts
- Delete contacts
- Use stored contacts in workflows

Example:

```text
Send email to Rahul
```

---

# API Endpoints

| Endpoint | Method | Description |
|---|---|---|
| / | GET | Health check |
| /run | POST | Run AI workflow |
| /tasks | GET | Get supported tasks |
| /contacts | GET | Fetch contacts |
| /contacts | POST | Add contact |
| /contacts/{id} | DELETE | Delete contact |
| /meetings | GET | Fetch meetings |

---

# Execution Tracking

The system tracks:

- Execution status
- Success/failure metrics
- Execution latency
- Request history
- Workflow logs
- LangSmith traces

---

# Retry Workflow

The executor includes retry handling for failed executions.

```text
Task
  ↓
Execute
  ↓
Success?
 ├── Yes → Complete
 └── No
        ↓
      Retry 1
        ↓
      Retry 2
        ↓
      Failure
```

---

# Current Capabilities

- Schedule meetings
- Send emails
- Contact management
- Workflow execution tracking
- Request history storage
- Retry handling
- Metrics tracking
- LangSmith tracing
- Structured validation
- Dynamic task routing

---

# Key Engineering Concepts Demonstrated

- AI workflow orchestration
- LangGraph state management
- LLM planning systems
- Structured validation pipelines
- Retry handling
- Dynamic tool execution
- Database-driven entity resolution
- Execution observability
- REST API development
- Full-stack AI application architecture

---

# Future Improvements

- PostgreSQL migration
- Async background execution
- Human approval workflows
- Multi-agent workflows
- Vector memory / RAG integration
- Kubernetes deployment

---

# Screenshots

## Streamlit UI

```text
screenshots/ui.png
```

## Contact Management

```text
screenshots/contacts.png
```

## FastAPI Swagger UI

```text
screenshots/swagger.png
```

## LangSmith Tracing

```text
screenshots/langsmith.png
```

## Architecture Diagram

```text
screenshots/architecture.png
```

## Workflow Diagram

```text
screenshots/workflow.png
```

## Deployment Diagram

```text
screenshots/deployment.png
```

---

# Deployment

| Service | Platform |
|---|---|
| FastAPI Backend | Render |
| Streamlit Frontend | Streamlit Community Cloud |

---

# Author

Dhanush Kumar