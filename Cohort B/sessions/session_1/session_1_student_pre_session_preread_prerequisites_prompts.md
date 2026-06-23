# Session 1 Student Pre-Session File: Build Core Backend — Ticket CRUD API

## What We Are Building

In this 8-session program, we will build one continuous, production-grade project:

# AI Support Ticket Resolution Copilot

This is a backend system that helps support teams manage, triage, and resolve support tickets using AI. You will build the entire stack from scratch — REST API, database layer, authentication, LLM integration, semantic search, and an autonomous resolution agent.

By the end of all 8 sessions, the system will be able to:

- accept and store support tickets via a REST API
- persist tickets in a PostgreSQL database with proper schema
- authenticate API requests using JWT tokens
- auto-categorize and prioritize tickets using OpenAI
- search for similar past tickets using semantic embeddings in ChromaDB
- retrieve solution suggestions using LangChain RAG
- autonomously resolve tickets using a LangGraph agent
- be deployed and monitored on a cloud platform

## Session 1 Goal

In Session 1, we build only the REST API layer. No database, no auth, no AI.

We will create a FastAPI backend with 5 endpoints for support ticket CRUD operations. Data is stored in-memory for now. The goal is to define a clean API contract that every future session will build on top of.

## Session 1 Output

By the end of Session 1, you will have:

- a running FastAPI application at `http://localhost:8000`
- 5 working REST endpoints for ticket management
- Pydantic models for input validation and response serialization
- auto-generated Swagger docs at `http://localhost:8000/docs`
- a clean project structure that will grow across all 8 sessions

---

# Pre-Read

## Why Are We Adding This Feature at This Point in the Build?

Every layer we add in this program depends on the layer below it. The REST API is the foundational contract — it defines what data the system accepts, what it returns, and how clients interact with it. Before we can add a database, we need to know what fields a ticket has. Before we can add JWT auth, we need routes to protect. Before we can call OpenAI, we need a ticket object to send to it.

Starting with the API also forces us to make explicit data model decisions early: What fields does a ticket need? Which fields does the server control vs the client? What does a valid vs invalid request look like? These decisions are much cheaper to change now than after we have a database schema, migrations, and downstream AI code depending on them.

This is how real backend systems are built — the API contract is negotiated first, then storage, then security, then business logic.

## System Architecture Flow

The complete system we are building across all 8 sessions:

```
Session 1 — REST API Layer
HTTP Client (Swagger / frontend / mobile)
        |
        v
FastAPI Application  ←  Pydantic Validation (422 on bad input)
        |
        v
APIRouter — /tickets
        |
        v
In-memory list  →  returns TicketResponse JSON
        |
        [Session 2 replaces in-memory with ↓]
        v
Session 2 — Database Layer
SQLModel ORM  →  SQLite / PostgreSQL
        |
        [Session 3 adds ↓]
        v
Session 3 — Authentication Layer
JWT Middleware  →  OAuth2PasswordBearer  →  Protected Routes
        |
        [Session 4 adds ↓]
        v
Session 4 — LLM Integration
OpenAI API  →  Auto-categorize + prioritize ticket
        |
        [Session 5 adds ↓]
        v
Session 5 — Semantic Search
OpenAI Embeddings  →  ChromaDB  →  Similarity Search
        |
        [Session 6 adds ↓]
        v
Session 6 — RAG Solution Retrieval
LangChain  →  Retrieve past solutions  →  Augmented response
        |
        [Session 7 adds ↓]
        v
Session 7 — Autonomous Agent
LangGraph  →  Classify → Search → Draft Solution → Escalate
        |
        [Session 8 adds ↓]
        v
Session 8 — Deployment and Monitoring
Docker  →  Cloud Platform  →  Logging  →  Health Checks
```

## Key Concepts to Revise Before Session 1

You have covered all of these in the program. Spend 10–15 minutes refreshing before class:

### 1. FastAPI Routing and Decorators

Know how `@app.get("/path")`, `@app.post("/path")`, `@app.patch("/path/{id}")`, `@app.delete("/path/{id}")` work. Know that FastAPI reads function parameter annotations to determine how to parse request data (path params, query params, body).

### 2. Pydantic BaseModel

Know how to define a `BaseModel` subclass with type-annotated fields, how `Optional[str] = None` makes a field optional, how `model_dump()` and `model_dump(exclude_unset=True)` behave differently, and what a `ValidationError` looks like.

### 3. HTTP Methods and Semantics

Know when to use GET (read), POST (create), PUT (full replace), PATCH (partial update), DELETE (remove). Know why we prefer PATCH over PUT for partial updates.

### 4. HTTP Status Codes

Know the meaning of: 200 (OK), 201 (Created), 204 (No Content), 400 (Bad Request), 404 (Not Found), 422 (Unprocessable Entity), 500 (Internal Server Error).

### 5. FastAPI APIRouter

Know how `APIRouter` works: you define routes on a router instance, then mount it on the main `FastAPI` app via `app.include_router()`. This allows you to split routes across multiple files.

### 6. UUID and datetime in Python

Know how to generate a UUID4 with `uuid.uuid4()` and convert it to string. Know how to get the current UTC time with `datetime.utcnow()`. These are used for server-generated ticket fields.

### 7. Python Type Hints with typing module

Refresh `Optional`, `List`, `Literal` from `typing`. Pydantic v2 uses these for validation logic. `Literal["open", "in_progress", "closed"]` restricts a field to one of those exact string values.

### 8. Project Structure for Python Backend

Know the difference between a module (`models.py`) and a package (`routes/` with `__init__.py`). Know how relative imports work: `from app.models import TicketCreate`.

## Technical Explanation

FastAPI is a modern Python web framework built on top of Starlette (ASGI) and Pydantic. It is not magic — when you write `def create_ticket(ticket: TicketCreate)`, FastAPI inspects the type annotation `TicketCreate` at startup and knows that the HTTP request body should be deserialized into that Pydantic model. At runtime, it calls `TicketCreate.model_validate(json_body)`, which performs all field validation. If validation fails, FastAPI catches the resulting `ValidationError` and converts it to a 422 HTTP response. Your function `create_ticket` is never called.

The `APIRouter` is a collection of route definitions. `app.include_router(router, prefix="/tickets")` does not copy code — it registers the router's routes with the app's route table at the specified prefix. This means a route `@router.get("/{id}")` becomes accessible at `/tickets/{id}`.

---

# Prerequisites

## Python Packages to Install Before Class

Run this before the session:

```bash
pip install fastapi uvicorn
```

Verify the install:

```bash
python -c "import fastapi; print(fastapi.__version__)"
python -c "import uvicorn; print(uvicorn.__version__)"
```

You do not need any database drivers, OpenAI SDK, or LangChain for Session 1.

## Environment Setup

1. Python 3.11 or higher installed (check: `python --version`)
2. A code editor: VS Code, PyCharm, or any editor that works with Claude Code / Cursor
3. Terminal access (not just an IDE terminal — a standalone terminal is useful for running `uvicorn`)
4. Claude Code CLI or Cursor IDE installed and authenticated
5. A browser for testing Swagger at `http://localhost:8000/docs`

## Code State From the Previous Session

This is Session 1 — there is no previous codebase. You are starting from an empty directory.

Create the project directory before class:

```bash
mkdir ai-support-copilot
cd ai-support-copilot
```

---

# Content to Prepare Before Class

Prepare this in a text file or have it ready to paste:

```text
Project name: AI Support Ticket Resolution Copilot

Session 1 scope: FastAPI REST API, 5 CRUD endpoints, in-memory storage only

Ticket fields:
- id: UUID string, server-generated
- title: str, required
- description: str, required
- category: str, optional (e.g., "billing", "technical", "general")
- priority: str, optional (e.g., "low", "medium", "high", "critical")
- status: str, server-controlled, default "open"
- created_at: datetime string, server-generated

Endpoints to build:
1. POST /tickets — create ticket, return 201
2. GET /tickets — list all tickets, return 200
3. GET /tickets/{id} — get one ticket, return 200 or 404
4. PATCH /tickets/{id} — update status, return 200 or 404
5. DELETE /tickets/{id} — delete ticket, return 204 or 404

What NOT to build in Session 1:
- No SQLModel, SQLAlchemy, or any database
- No JWT or authentication
- No OpenAI or LLM calls
- No background tasks or WebSockets
- No Docker or deployment
```

---

# Prompts for Session 1

Use these prompts during the session when instructed by your instructor. All prompts are designed for Claude Code or Cursor AI coding tools.

---

## Prompt 1: Main Build Prompt

```text
I am building an AI Support Ticket Resolution Copilot using FastAPI (Python). This is Session 1 of an 8-session project.

Current state of the project: EMPTY. There is no existing code. I am starting from scratch.

Build the following FastAPI REST API with exactly this file structure:

ai-support-copilot/
├── main.py
├── models.py
└── routes/
    ├── __init__.py
    └── tickets.py

WHAT TO BUILD:

1. models.py — Pydantic schemas only, no SQLModel, no database imports
   - TicketCreate(BaseModel): fields: title (str, required), description (str, required), category (Optional[str] = None), priority (Optional[str] = None)
   - TicketUpdate(BaseModel): fields: title (Optional[str] = None), description (Optional[str] = None), category (Optional[str] = None), priority (Optional[str] = None), status (Optional[Literal["open", "in_progress", "resolved", "closed"]] = None)
   - TicketResponse(BaseModel): fields: id (str), title (str), description (str), category (Optional[str]), priority (Optional[str]), status (str), created_at (str)

2. routes/tickets.py — APIRouter with 5 endpoints
   - In-memory storage: tickets_db: list[dict] = [] at module level
   - POST / — create ticket, generate UUID with uuid.uuid4(), set status="open", set created_at=datetime.utcnow().isoformat(), append to tickets_db, return TicketResponse with status_code=status.HTTP_201_CREATED
   - GET / — return all tickets in tickets_db as List[TicketResponse], status_code=200
   - GET /{ticket_id} — find ticket by id, return TicketResponse or raise HTTPException(status_code=404, detail="Ticket not found")
   - PATCH /{ticket_id} — find ticket by id, update only the fields provided using update_data.model_dump(exclude_unset=True), return updated TicketResponse or 404
   - DELETE /{ticket_id} — find ticket by id, remove from tickets_db, return Response with status_code=204, or raise HTTPException 404 if not found
   - Router must NOT have a prefix — prefix will be set in main.py

3. main.py — FastAPI app setup only
   - Create FastAPI app: app = FastAPI(title="AI Support Ticket Copilot", version="1.0.0")
   - Import and include the tickets router: app.include_router(tickets_router, prefix="/tickets", tags=["tickets"])
   - Add a root health check: GET / returns {"status": "ok", "message": "AI Support Ticket Copilot is running"}

4. routes/__init__.py — empty file

REQUIREMENTS:
- Use fastapi, fastapi.responses, fastapi.routing, pydantic, uuid, datetime, typing imports only
- Do NOT add SQLModel, SQLAlchemy, databases, asyncpg, or any database library
- Do NOT add JWT, OAuth2, or any authentication
- Do NOT add OpenAI, LangChain, or any AI library
- Do NOT add background tasks or WebSocket handlers
- Do NOT add custom exception middleware
- Use status_code=status.HTTP_201_CREATED for POST
- Use status_code=status.HTTP_204_NO_CONTENT with Response() for DELETE (no body)
- Use HTTPException for all 404 responses
- Add a comment above each function explaining what it does and what it returns
- Add a comment explaining the tickets_db variable and its limitation as in-memory storage

VERIFY: After generation, confirm that uvicorn main:app --reload starts without errors and Swagger at http://localhost:8000/docs shows all 5 endpoints.
```

---

## Prompt 2: Improvement Prompt

```text
The FastAPI ticket API is working. Now refactor it for cleaner code and better error handling without changing the API contract.

Current issues to fix:

1. In routes/tickets.py, the linear search for ticket by ID is repeated in GET /{id}, PATCH /{id}, and DELETE /{id}. Extract it into a helper function:
   def get_ticket_or_404(ticket_id: str) -> dict:
       ticket = next((t for t in tickets_db if t["id"] == ticket_id), None)
       if ticket is None:
           raise HTTPException(status_code=404, detail=f"Ticket with id '{ticket_id}' not found")
       return ticket
   
   Refactor all three endpoints to use this helper.

2. In models.py, add field validation to TicketCreate:
   - title: min_length=3, max_length=200
   - description: min_length=10
   - priority: restrict to Literal["low", "medium", "high", "critical"] or None
   - category: restrict to Literal["billing", "technical", "account", "general"] or None

3. In main.py, add a GET /tickets/health endpoint that returns a count of tickets:
   {"status": "ok", "ticket_count": len(tickets_db)}
   
   Note: this must be defined BEFORE the /{ticket_id} route or FastAPI will try to match "health" as a ticket_id.

4. In all response models, ensure the PATCH endpoint returns the complete updated ticket, not just the fields that changed.

Do NOT change the HTTP methods, URL paths, or status codes. The API contract must remain the same.
Show the complete updated files, not just diffs.
```

---

## Prompt 3: Debugging Prompt — 422 Validation Error and 404 Not Found

```text
I am debugging my FastAPI ticket API. I am hitting two specific issues.

ISSUE 1: I am getting a 422 Unprocessable Entity when I POST to /tickets with this body:
{
  "title": "Login page broken",
  "description": "The login page returns a 500 error",
  "priority": 1
}

Expected: 201 Created with the ticket
Actual: 422 with a validation error about the priority field

Please:
1. Show me the exact Pydantic validation error that FastAPI would return for this input
2. Explain why priority=1 (integer) fails if the model declares priority as Optional[str]
3. Fix the request body so it passes validation
4. If I want to accept both integers (1=low, 2=medium etc.) and strings ("low", "medium"), show me how to add a Pydantic validator that handles both

ISSUE 2: After creating a ticket, I call GET /tickets/{id} with the UUID from the POST response and get 404.

My POST response was:
{
  "id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
  "title": "Login page broken",
  ...
}

I then call: GET /tickets/3fa85f64-5717-4562-b3fc-2c963f66afa6

And get: {"detail": "Ticket not found"}

Possible causes to investigate:
1. Is the ticket ID stored as a UUID object but compared as a string?
2. Is there a route prefix conflict causing the wrong endpoint to be matched?
3. Is the in-memory tickets_db list being reset between requests (e.g., reinstantiated on each import)?

Diagnose the most likely cause given this code pattern and show the fix.
```

---

## Prompt 4: Code Explanation Prompt

```text
Explain the generated FastAPI ticket API code for interview preparation. I need to understand it technically, not just at a high level.

Walk through each file and explain:

main.py:
- What does FastAPI(title="...", version="...") do at the class level?
- What exactly does app.include_router(tickets_router, prefix="/tickets", tags=["tickets"]) register?
- Why does the health check route go in main.py and not in routes/tickets.py?

models.py:
- Why is TicketCreate a separate class from TicketResponse? Why not one model?
- What does Optional[str] = None mean in Pydantic v2 vs Pydantic v1?
- Why is status not a field in TicketCreate?
- What does model_dump(exclude_unset=True) return differently from model_dump()?

routes/tickets.py:
- Walk through the full execution path when POST /tickets is called with a valid body
- Walk through the full execution path when GET /tickets/{id} is called with a non-existent ID
- Why does DELETE return Response(status_code=204) instead of returning a dict?
- What is the type annotation List[TicketResponse] doing in the GET /tickets return type?

For each explanation, give me the exact technical answer I would give in an interview — not a tutorial-style explanation.
```

---

## Prompt 5: Interview Explanation Prompt

```text
I am preparing to explain this FastAPI project in a technical interview. Help me build concise, accurate answers.

For each question below, give me a 3-5 sentence interview-ready answer that uses correct technical terminology:

1. "Walk me through the architecture of this backend API."

2. "Why did you choose FastAPI over Flask for this project?"

3. "What does Pydantic do in this project and where does it run in the request lifecycle?"

4. "If a client sends a POST request without the title field, what HTTP response do they get and why?"

5. "You're using in-memory storage. What are the failure modes of this approach in production?"

6. "Why does your PATCH endpoint use exclude_unset=True? What happens if you don't?"

7. "What is the difference between a 404 and a 422 response in your API?"

8. "How does FastAPI generate the Swagger documentation at /docs?"

For each answer, flag which part of the answer demonstrates understanding vs just usage knowledge. Interviewers want to see the "why", not just the "what".
```

---

## Prompt 6: Unit Test Generation Prompt

```text
Generate a complete pytest test suite for the FastAPI ticket CRUD API.

The API has these endpoints:
- POST /tickets — create ticket, returns 201
- GET /tickets — list all tickets, returns 200
- GET /tickets/{id} — get one ticket, returns 200 or 404
- PATCH /tickets/{id} — update status or other fields, returns 200 or 404
- DELETE /tickets/{id} — delete ticket, returns 204 or 404

Generate tests/test_tickets.py with the following:

SETUP:
- Use FastAPI TestClient: from fastapi.testclient import TestClient
- Import app from main
- client = TestClient(app)
- Add a pytest fixture that clears tickets_db before each test to ensure test isolation

TEST CASES — write a separate test function for each:

1. test_create_ticket_success — POST valid body, assert 201, assert response has id, title, status="open", created_at
2. test_create_ticket_missing_title — POST without title, assert 422, assert "title" in response error detail
3. test_create_ticket_missing_description — POST without description, assert 422
4. test_list_tickets_empty — GET /tickets with no tickets, assert 200 and response == []
5. test_list_tickets_returns_created — create a ticket then GET /tickets, assert length 1 and ticket is in list
6. test_get_ticket_by_id_success — create ticket, GET /tickets/{id}, assert 200 and correct title
7. test_get_ticket_by_id_not_found — GET /tickets/nonexistent-uuid, assert 404
8. test_patch_ticket_status — create ticket, PATCH with {"status": "in_progress"}, assert 200 and status updated
9. test_patch_ticket_does_not_overwrite_other_fields — create ticket, PATCH with {"status": "resolved"}, assert title is unchanged
10. test_patch_ticket_not_found — PATCH /tickets/nonexistent-uuid, assert 404
11. test_delete_ticket_success — create ticket, DELETE /tickets/{id}, assert 204 and no response body
12. test_delete_ticket_not_found — DELETE /tickets/nonexistent-uuid, assert 404
13. test_delete_then_get_returns_404 — create ticket, delete it, then GET /tickets/{id}, assert 404

For each test, add a one-line comment explaining what the test is verifying and why it matters.

Do NOT use mocking for the in-memory storage — test against the real in-memory list.
```

---

## Prompt 7: Edge Case and Error State Prompt

```text
The basic ticket CRUD API is working. Now add proper edge case handling and hardening.

Add the following to the existing codebase:

1. VALIDATE STATUS TRANSITIONS in PATCH /tickets/{id}:
   Only allow these transitions:
   - open → in_progress
   - open → closed
   - in_progress → resolved
   - in_progress → closed
   - resolved → closed
   
   If the requested transition is invalid (e.g., resolved → open), raise:
   HTTPException(status_code=422, detail=f"Invalid status transition from '{current_status}' to '{new_status}'")
   
   Add a constant VALID_TRANSITIONS: dict[str, list[str]] in routes/tickets.py.

2. PREVENT DUPLICATE TITLES in POST /tickets:
   Before creating a ticket, check if a ticket with the same title (case-insensitive) already exists.
   If yes, raise HTTPException(status_code=409, detail="A ticket with this title already exists")

3. ADD QUERY PARAMETERS to GET /tickets:
   Support optional filtering:
   - GET /tickets?status=open — return only open tickets
   - GET /tickets?priority=high — return only high priority tickets
   - GET /tickets?category=billing — return only billing tickets
   
   Implement using FastAPI Query parameters with Optional[str] = None defaults.
   Return filtered list or full list if no filter is provided.

4. ADD PAGINATION to GET /tickets:
   Support: GET /tickets?skip=0&limit=10
   - skip: int = Query(default=0, ge=0)
   - limit: int = Query(default=10, ge=1, le=100)
   Apply after filtering.

5. HARDEN DELETE:
   Return 204 correctly — FastAPI sometimes sends a response body if you return a dict with 204.
   Ensure the DELETE endpoint uses: return Response(status_code=status.HTTP_204_NO_CONTENT)
   Do not return any dict or message body.

Show the complete updated routes/tickets.py and models.py. Do not change main.py unless strictly necessary.
```

---

# What You Should Be Able to Explain After Session 1

By the end of the session, you should be able to answer these questions without looking at your notes:

1. What are the 5 endpoints in this API, what HTTP method does each use, and what status code does each return on success?
2. Why is there a `TicketCreate` model separate from `TicketResponse`? What is in each one and why?
3. What happens at each layer of the request lifecycle when a client sends `POST /tickets` with an invalid request body?
4. What is `exclude_unset=True` and why is it critical for the PATCH endpoint?
5. Why does `DELETE /tickets/{id}` return 204 instead of 200?
6. What is the difference between `APIRouter` and the main `FastAPI` app, and what does `include_router` do?
7. What are two production-critical limitations of storing tickets in a Python list instead of a database?
8. How does FastAPI generate Swagger documentation — what does it inspect and when?
9. What exact HTTP response does Pydantic produce when a required field is missing, and what is in the response body?
10. If you ran this server with `--workers 4`, what would happen to tickets created by different requests? Why?

## Final Session 1 Explanation

```text
I built the REST API layer of an AI Support Ticket Resolution Copilot using FastAPI. The API exposes 5 CRUD endpoints for managing support tickets — create, list, get by ID, update status, and delete. Request bodies are validated by Pydantic models before reaching the route handler, which means clients get a detailed 422 error automatically if they send invalid data. Data is stored in an in-memory Python list for this session, which will be replaced by a SQLModel + PostgreSQL database in Session 2. The API auto-generates Swagger documentation at /docs and is structured with a clean separation between models, routes, and the application entry point, making it ready to extend with authentication, LLM integration, and deployment in later sessions.
```
