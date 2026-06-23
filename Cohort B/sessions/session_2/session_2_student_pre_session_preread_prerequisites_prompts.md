# Session 2 Student Pre-Session File: Add Database Layer + Data Modeling

## What We Are Building

Over the course of this program, we are building one continuous backend system:

# AI Support Ticket Resolution Copilot

This system will allow users to submit support tickets and get AI-assisted resolution suggestions.

By the end of all sessions, the backend will:

- accept and persist support tickets via a REST API
- enforce authentication and role-based access (admin vs user)
- classify and summarize tickets using an LLM
- retrieve similar past tickets using vector search (embeddings + ChromaDB)
- run a multi-step resolution agent using LangGraph
- expose a streaming resolution endpoint

## What We Added in Session 1

In Session 1 we built the core FastAPI backend with 5 CRUD endpoints operating on an in-memory Python list:

- `POST /tickets` — create a new ticket
- `GET /tickets` — list all tickets
- `GET /tickets/{id}` — get a ticket by ID
- `PUT /tickets/{id}` — update a ticket
- `DELETE /tickets/{id}` — delete a ticket

The `Ticket` was a Pydantic model stored in `tickets_db: list[dict]` — a module-level variable that reset to empty every time uvicorn restarted.

## Session 2 Goal

Replace the in-memory list with a persistent SQLite database using SQLModel as the ORM. After this session:

- tickets are stored in a file called `tickets.db` on disk
- all 5 endpoints read from and write to the database
- data survives server restarts
- the `Ticket` class is both a database table and a Pydantic validation model

## Session 2 Output

By the end of Session 2, your project should have:

1. A `Ticket` SQLModel table with `id`, `title`, `description`, `status`, `priority`, `created_at`, `updated_at`
2. A SQLite engine configured with `create_engine("sqlite:///./tickets.db")`
3. A `get_session` dependency function injected into all 5 endpoints
4. All 5 endpoints using `db.add()`, `db.commit()`, `db.refresh()`, `db.get()`, `db.exec()`, `db.delete()`
5. Table initialization via `SQLModel.metadata.create_all(engine)` on app startup
6. Verified persistence: restart uvicorn, GET /tickets still returns previously created tickets

---

# Pre-Read

## Why Are We Adding This Feature Now?

The in-memory list from Session 1 was intentionally minimal — it let us focus on FastAPI routing, Pydantic models, and HTTP semantics without the overhead of database setup. But it has a fundamental flaw: state is process-bound. Every time uvicorn restarts — for a code change, a server crash, a deployment — all ticket data is lost.

Any real backend system requires a persistence layer. The database is the contract that all other layers depend on:

- Session 3 auth needs to look up users and associate tickets with user IDs — this requires a persistent user table
- Session 4 LLM classification needs to read ticket descriptions and write back classification results — this requires database reads and writes
- Session 5 vector search needs to know which tickets exist to build and query the embedding index — this requires persistent ticket records

We add the database now because everything after Session 2 builds on top of it.

## System Architecture Flow

After Session 2, the full request flow for ticket creation looks like this:

```
HTTP POST /tickets (JSON body)
        |
    FastAPI Route Handler
        |
    Pydantic Validation (TicketCreate model)
        |
    Depends(get_session) — fresh DB session opened
        |
    Ticket.model_validate(ticket_in) — create SQLModel object
        |
    db.add(ticket) — stage in session unit of work
        |
    db.commit() — INSERT INTO ticket (...) VALUES (...)
        |
    db.refresh(ticket) — re-read row, get assigned id + timestamps
        |
    DB Session closed (context manager exit)
        |
HTTP 201 Response (TicketResponse JSON)
        |
    [tickets.db file updated on disk]
```

Future sessions will extend this flow:

```
Session 1: FastAPI in-memory CRUD
Session 2: FastAPI --> SQLModel ORM --> SQLite (tickets.db)
Session 3: FastAPI --> JWT Auth --> SQLModel ORM --> SQLite
Session 4: FastAPI --> JWT Auth --> SQLModel + LLM Classification --> SQLite
Session 5: FastAPI --> JWT Auth --> SQLModel + Embeddings --> SQLite + ChromaDB
Session 6+: FastAPI --> LangGraph Agent --> SQLModel + LLM + RAG --> SQLite + ChromaDB
```

## Key Concepts to Revise Before Class

### 1. SQLModel and Its Dual Role

SQLModel is a Python library by Sebastián Ramírez (same author as FastAPI). It wraps SQLAlchemy for the ORM layer and Pydantic for validation. A single class with `table=True` becomes both a database table definition and a Pydantic model.

Revise:
- `class Ticket(SQLModel, table=True)` — the `table=True` flag is what registers the class as a database table
- `Field(primary_key=True)` — marks the column as the table's primary key
- `Optional[int] = Field(default=None, primary_key=True)` — why the PK must be `Optional` before insert
- `default_factory` vs `default` in `Field()` — `default_factory=datetime.utcnow` is evaluated at insert time; `default=datetime.utcnow()` is evaluated once when the class is defined

### 2. SQLAlchemy Session Lifecycle

The Session is the core object you interact with for all database operations. Key operations:
- `db.add(obj)` — marks an object as pending (to be inserted or updated)
- `db.commit()` — flushes all pending changes to the database as a transaction
- `db.refresh(obj)` — reloads the object from the database (picks up DB-generated values)
- `db.get(Model, pk)` — fetches a single row by primary key; returns `None` if not found
- `db.exec(select(Model))` — executes a SQLAlchemy select statement; returns a result set
- `db.delete(obj)` — marks an object for deletion; must still be followed by `db.commit()`

### 3. FastAPI Dependency Injection

FastAPI's `Depends()` is a mechanism for injecting shared resources into endpoint functions. You define a dependency function (which can be a generator), and FastAPI calls it before running your endpoint, passes the result in, and tears it down after the request completes.

Pattern to understand:
```python
def get_session():
    with Session(engine) as session:
        yield session  # FastAPI injects the yielded value into the endpoint

@app.get("/tickets")
def list_tickets(db: Session = Depends(get_session)):
    ...
```

The `yield` pattern means "use this and then clean up." After the endpoint returns, FastAPI continues past the `yield`, triggering the `with` block's cleanup and closing the session.

### 4. SQLite as a Database Engine

SQLite is a serverless, file-based relational database. The entire database is stored in a single `.db` file. No separate database server needs to run. It supports standard SQL and full ACID transactions. It is bundled with Python (`import sqlite3`).

Connection URL format: `sqlite:///./tickets.db` — three slashes for relative path, four for absolute path (`sqlite:////tmp/tickets.db`).

Key limitation: SQLite uses file-level locking for writes, so it does not support concurrent write transactions. For a single-process development server this is fine. For production with multiple workers, PostgreSQL is required.

### 5. Primary Keys and Auto-Increment

In a relational database, every table has a primary key — a column (or set of columns) that uniquely identifies each row. Using an auto-increment integer primary key means the database assigns the ID at insert time. You do not specify it in the `INSERT` statement; the database calculates and assigns the next available integer.

This is why in the `Ticket` model, `id` starts as `None` (before insert) and is populated by SQLite after `db.commit()` + `db.refresh()`.

### 6. The `select()` Query Builder

To fetch multiple rows, use `select()` from `sqlmodel`:

```python
from sqlmodel import select

statement = select(Ticket)
results = db.exec(statement)
tickets = results.all()
```

You can chain `.where()` clauses:
```python
statement = select(Ticket).where(Ticket.status == "open")
```

### 7. Alembic vs `create_all`

`SQLModel.metadata.create_all(engine)` is a development shortcut that creates all tables that do not exist. It is idempotent but cannot alter existing tables. If you add a new column to the model and run `create_all` again, the column will not be added to the existing database table.

Alembic is the production-grade migration tool for SQLAlchemy projects. It generates versioned migration scripts that can `upgrade` (apply a schema change) or `downgrade` (revert it). For Session 2, use `create_all`. You will encounter Alembic in more advanced deployments.

### 8. `model_validate()` vs Direct Instantiation

When converting a Pydantic input model (e.g., `TicketCreate`) to a SQLModel table instance (e.g., `Ticket`), use:

```python
db_ticket = Ticket.model_validate(ticket_in)
```

This copies all shared fields from the Pydantic model to the SQLModel instance. It is equivalent to `Ticket(**ticket_in.model_dump())` but is the idiomatic SQLModel approach and handles nested models correctly.

---

# Prerequisites: Setup Before Class

## Python Packages to Install

Run this before the session:

```bash
pip install sqlmodel
```

SQLModel installs SQLAlchemy and Pydantic as dependencies automatically. Verify:

```bash
python -c "import sqlmodel; print(sqlmodel.__version__)"
```

You should also have these already installed from Session 1:

```bash
pip install fastapi uvicorn[standard] pydantic
```

If you want to inspect the SQLite database file visually, install DB Browser for SQLite:
- macOS: `brew install --cask db-browser-for-sqlite`
- Windows: download from https://sqlitebrowser.org/

Alternatively, you can use the SQLite CLI:
```bash
sqlite3 tickets.db "SELECT * FROM ticket;"
```

## Environment Setup

Ensure your Session 1 project is in the following state before class:

- `app/main.py` — FastAPI app with 5 in-memory CRUD endpoints
- `app/models.py` — Pydantic models (`TicketCreate`, `TicketResponse`, `TicketUpdate`)
- `requirements.txt` — contains `fastapi`, `uvicorn`, `pydantic`
- uvicorn runs with `uvicorn app.main:app --reload` from project root
- Swagger UI at http://127.0.0.1:8000/docs is accessible and all 5 endpoints are visible

## Code State From Session 1

Your `app/main.py` should look approximately like this (simplified):

```python
from fastapi import FastAPI, HTTPException
from app.models import TicketCreate, TicketResponse, TicketUpdate
from typing import List

app = FastAPI()

tickets_db: list[dict] = []
ticket_counter: int = 1

@app.post("/tickets", response_model=TicketResponse, status_code=201)
def create_ticket(ticket: TicketCreate):
    global ticket_counter
    new_ticket = {"id": ticket_counter, **ticket.model_dump()}
    tickets_db.append(new_ticket)
    ticket_counter += 1
    return new_ticket

@app.get("/tickets", response_model=List[TicketResponse])
def list_tickets():
    return tickets_db

# ... GET by id, PUT, DELETE endpoints
```

This is what we are replacing today.

---

# Content to Prepare Before Class

Have the following file structure planned before class. Session 2 will refactor the project into this layout:

```
ai-support-copilot/
├── app/
│   ├── __init__.py
│   ├── main.py          # FastAPI app, startup event, endpoint registration
│   ├── models.py        # SQLModel Ticket table + Pydantic input/output schemas
│   └── database.py      # engine, create_db_and_tables(), get_session()
├── tickets.db           # auto-created by SQLModel on first run (do not commit this)
├── requirements.txt
└── .gitignore           # add tickets.db to this
```

Add `tickets.db` to your `.gitignore` before class:

```
tickets.db
__pycache__/
*.pyc
.env
```

---

# Prompts for Session 2

Use these prompts during the session when instructed by the instructor. All prompts are designed for Antigravity. Paste them directly.

---

## Prompt 1: Main Build Prompt

```text
I am building an AI Support Ticket Resolution Copilot backend using Python and FastAPI.

Project context:
- This is a multi-session build. Session 1 is complete. Session 2 is the current session.
- Session 1 deliverable: A FastAPI app with 5 CRUD endpoints (POST, GET list, GET by id, PUT, DELETE) operating on an in-memory Python list called `tickets_db`.
- Session 2 goal: Replace the in-memory list with a persistent SQLite database using SQLModel as the ORM.

Current project file structure:
- app/main.py — FastAPI app with 5 in-memory CRUD endpoints and in-memory ticket list
- app/models.py — Pydantic models: TicketCreate, TicketResponse, TicketUpdate

Task: Refactor the project to add a database layer with the following exact structure:

File: app/database.py
- Import: from sqlmodel import create_engine, Session, SQLModel
- Create engine: DATABASE_URL = "sqlite:///./tickets.db", engine = create_engine(DATABASE_URL, echo=True, connect_args={"check_same_thread": False})
- Function: create_db_and_tables() that calls SQLModel.metadata.create_all(engine)
- Generator function: get_session() that uses `with Session(engine) as session: yield session`

File: app/models.py
- Replace existing Pydantic Ticket model with a SQLModel table class
- Define: class Ticket(SQLModel, table=True) with these exact fields:
  - id: Optional[int] = Field(default=None, primary_key=True)
  - title: str
  - description: str
  - status: str = Field(default="open")
  - priority: str = Field(default="medium")
  - created_at: datetime = Field(default_factory=datetime.utcnow)
  - updated_at: datetime = Field(default_factory=datetime.utcnow)
- Keep TicketCreate as a separate SQLModel (no table=True) with: title, description, priority (optional, default "medium")
- Keep TicketUpdate as a separate SQLModel (no table=True) with all fields Optional: title, description, status, priority
- Keep TicketResponse as a SQLModel (no table=True) with: id, title, description, status, priority, created_at, updated_at

File: app/main.py
- Remove the in-memory tickets_db list and ticket_counter
- Import create_db_and_tables and get_session from app.database
- Import Session from sqlmodel, Depends from fastapi, select from sqlmodel
- Add startup event or lifespan handler that calls create_db_and_tables()
- Update all 5 endpoints to use db: Session = Depends(get_session):
  - POST /tickets: Ticket.model_validate(ticket_in), db.add(), db.commit(), db.refresh(), return ticket
  - GET /tickets: db.exec(select(Ticket)).all()
  - GET /tickets/{ticket_id}: db.get(Ticket, ticket_id), raise HTTPException(404) if None
  - PUT /tickets/{ticket_id}: db.get(), raise 404 if None, use model_dump(exclude_unset=True) + setattr loop, set updated_at=datetime.utcnow(), db.add(), db.commit(), db.refresh()
  - DELETE /tickets/{ticket_id}: db.get(), raise 404 if None, db.delete(), db.commit(), return Response(status_code=204)

Requirements:
- Import datetime from datetime module in models.py
- Import Optional from typing in models.py
- Use from sqlmodel import SQLModel, Field, select in appropriate files
- All endpoints must have correct response_model and status_code
- Add a brief inline comment above each db operation explaining what it does
- Do NOT add: PostgreSQL config, async sessions, User table, authentication, Alembic setup, Redis, background tasks
- Do NOT use deprecated Pydantic v1 validators (@validator) — use Field() defaults only
- Do NOT add any endpoints beyond the original 5 CRUD routes

After generating all files, provide a one-paragraph explanation of the session lifecycle (add -> commit -> refresh) in plain Python terms.
```

---

## Prompt 2: Improvement Prompt

```text
Review the current Session 2 FastAPI + SQLModel codebase and improve it in the following ways:

1. Error handling: Ensure all endpoints that accept a ticket_id path parameter raise HTTPException(status_code=404, detail="Ticket not found") when db.get(Ticket, ticket_id) returns None. Check GET, PUT, and DELETE.

2. PUT endpoint: Confirm it uses model_dump(exclude_unset=True) and a setattr loop so only explicitly provided fields are updated. Confirm it sets ticket.updated_at = datetime.utcnow() before commit.

3. Response models: Confirm all 5 endpoints have an explicit response_model declared. POST should return status_code=201, DELETE should return status_code=204 with no response body.

4. engine config: Add connect_args={"check_same_thread": False} to create_engine() if it is missing. This is required for SQLite when used with FastAPI's multi-threaded request handling.

5. Startup: Confirm create_db_and_tables() is called at app startup using either @app.on_event("startup") or the modern lifespan context manager pattern. It must run before any endpoint is called.

6. Code comments: Add a one-line comment above each database operation (db.add, db.commit, db.refresh, db.get, db.exec, db.delete) explaining what that operation does. This is for interview and code review readiness.

Do not add any new endpoints, tables, or features. Only improve the quality of the existing code.
```

---

## Prompt 3: Debugging Prompt — Session Not Committed / 404 After Correct ID

```text
I am debugging an issue in my FastAPI + SQLModel backend.

Symptom: I call POST /tickets and receive a 201 response with a valid JSON body including an id field. But when I immediately call GET /tickets/{id} using that same id, I receive a 404 "Ticket not found" error.

I also notice that when I restart uvicorn and call GET /tickets, the response is an empty list even though I created tickets before the restart.

My endpoint code:

    @app.post("/tickets", response_model=TicketResponse, status_code=201)
    def create_ticket(ticket: TicketCreate, db: Session = Depends(get_session)):
        db_ticket = Ticket.model_validate(ticket)
        db.add(db_ticket)
        db.refresh(db_ticket)
        return db_ticket

Please diagnose this code:
1. Identify the exact bug (missing operation)
2. Explain why the 201 response shows an id despite the bug
3. Show the corrected endpoint with the fix applied
4. Explain in 2-3 sentences what db.commit() does and why it is required before db.refresh()
5. Do not change any other part of the codebase — only fix this endpoint
```

---

## Prompt 4: Code Explanation Prompt

```text
Explain the following Session 2 FastAPI + SQLModel code in technical language suitable for a backend engineering interview.

For each file, explain:
1. What the file's responsibility is in the overall architecture
2. What each key line or block does at the Python/SQLAlchemy level
3. What would break if that line were removed or changed incorrectly

Focus on these specific areas:
- Why Ticket has table=True and what it changes about the class
- Why id is Optional[int] and when it becomes a real integer
- What create_engine() does and what echo=True means in production vs development
- What the yield in get_session() does and how FastAPI uses it
- The sequence: db.add() -> db.commit() -> db.refresh() — what SQL runs at each step
- What db.exec(select(Ticket)).all() translates to in SQL
- What exclude_unset=True does in the PUT endpoint and why it prevents data loss

Do not simplify or use non-technical analogies. The explanation should be at the level of a mid-level Python backend engineer explaining to a peer.
```

---

## Prompt 5: Interview Explanation Prompt

```text
I am preparing for a backend engineering interview. I need to explain the database layer I added to my FastAPI project in Session 2.

Generate an interview-ready explanation covering:

1. What I added: the specific components added in Session 2 (SQLModel table, engine, session factory, updated endpoints)

2. Why I made these choices:
   - Why SQLModel instead of raw SQLAlchemy or plain SQL
   - Why SQLite for development
   - Why dependency injection for the session instead of a global session
   - Why create_all instead of Alembic at this stage

3. The trade-offs I am aware of:
   - SQLite vs PostgreSQL for production
   - ORM vs raw SQL for complex queries
   - create_all vs Alembic for schema evolution

4. What could go wrong and how I handle it:
   - 404 when ticket ID does not exist
   - Session not committed (data appears in response but not in DB)
   - Schema changes breaking the existing database

5. What comes next: how the database layer enables Session 3 (auth) and Session 4 (LLM features)

Format the explanation as if I am speaking to a senior engineer in a 3-4 minute verbal answer. Be technically precise — use correct Python and SQL terminology.
```

---

## Prompt 6: Unit Test Generation Prompt

```text
Generate a complete pytest test file for the Session 2 FastAPI + SQLModel backend.

Project context:
- FastAPI app in app/main.py
- SQLModel Ticket table in app/models.py
- Database engine and get_session in app/database.py
- 5 endpoints: POST /tickets, GET /tickets, GET /tickets/{id}, PUT /tickets/{id}, DELETE /tickets/{id}

Requirements for the test file:
- File path: tests/test_tickets.py
- Use pytest and FastAPI's TestClient from fastapi.testclient
- Override the get_session dependency to use an in-memory SQLite database: create_engine("sqlite:///:memory:") so tests do not write to the real tickets.db file
- Use SQLModel.metadata.create_all(engine) in a pytest fixture to initialize tables before each test
- Use a pytest fixture named `client` that returns a TestClient with the session override applied
- Use a pytest fixture named `sample_ticket_payload` that returns a dict with title, description, priority

Write tests for:
1. test_create_ticket_returns_201 — POST with valid payload, assert status 201, assert id is not None, assert title matches
2. test_create_ticket_missing_title_returns_422 — POST without title field, assert status 422
3. test_list_tickets_empty — GET /tickets on empty DB, assert status 200, assert response is empty list
4. test_list_tickets_after_create — create a ticket then GET /tickets, assert list has 1 item
5. test_get_ticket_by_id — create ticket, then GET /tickets/{id}, assert 200 and correct title
6. test_get_ticket_not_found — GET /tickets/99999, assert 404
7. test_update_ticket_status — create ticket, PUT /tickets/{id} with {"status": "in_progress"}, assert 200 and status updated
8. test_update_ticket_partial — PUT with only status field, assert title is unchanged (exclude_unset behavior)
9. test_delete_ticket — create ticket, DELETE /tickets/{id}, assert 204, then GET /tickets/{id} assert 404
10. test_delete_ticket_not_found — DELETE /tickets/99999, assert 404

Add a clear comment above each test explaining what behavior it is verifying.
Do not mock the database — use the in-memory SQLite override via dependency injection.
```

---

## Prompt 7: Edge Case and Error State Prompt

```text
Review my Session 2 FastAPI + SQLModel backend and add comprehensive edge case handling.

Current state: The 5 CRUD endpoints work for the happy path. I need to add handling for these specific edge cases:

1. POST /tickets with an empty string for title (e.g., {"title": "", "description": "test"}):
   - Should return 422 with a clear validation error
   - Add a Field validator or Pydantic validator to reject empty strings for title and description
   - Use Field(min_length=1) syntax, not the deprecated @validator decorator

2. GET /tickets with query parameter filters (optional enhancement):
   - Add optional query params: status: Optional[str] = None, priority: Optional[str] = None
   - If provided, filter the select() query with .where() clauses
   - If not provided, return all tickets (existing behavior preserved)

3. PUT /tickets/{id} with an invalid status value (e.g., {"status": "banana"}):
   - The current model accepts any string. Add a status field validator that only accepts: "open", "in_progress", "resolved", "closed"
   - Return 422 with detail: "status must be one of: open, in_progress, resolved, closed"
   - Use a Pydantic Literal type or a custom validator — not a bare string field

4. Database connection error handling:
   - Wrap the startup create_db_and_tables() call in a try/except
   - Log the error and re-raise if the database cannot be initialized

5. Confirm all existing 404 guards are in place for GET, PUT, and DELETE by id.

Do not add new tables, new endpoints, or authentication. Only add validation and error handling to the existing 5 endpoints and models.
Show the exact updated field definitions and endpoint code for each change.
```

---

# What You Should Be Able to Explain After Session 2

By the end of the session, you should be able to answer these questions without reading the code:

1. What is the difference between a SQLModel class with `table=True` and one without it?
2. Why is the `id` field typed as `Optional[int]` in the Ticket model?
3. What is the difference between `db.add()`, `db.commit()`, and `db.refresh()` — what SQL runs at each step?
4. What does `Depends(get_session)` do in a FastAPI endpoint, and what happens to the session after the response is sent?
5. Why must each HTTP request get its own database session rather than sharing a global one?
6. What does `SQLModel.metadata.create_all(engine)` do, and what does it NOT do?
7. What is the difference between SQLite and PostgreSQL from a production deployment perspective?
8. Why does the PUT endpoint use `model_dump(exclude_unset=True)` and what would break without it?
9. What SQL query does `db.exec(select(Ticket)).all()` correspond to?
10. When would you use Alembic instead of `create_all`, and what is the difference?

## Final Session 2 Explanation

```text
In Session 2 I replaced the in-memory Python list from Session 1 with a persistent SQLite database using SQLModel as the ORM. I defined a Ticket class with table=True that serves as both the database table definition and the Pydantic validation schema. I configured a SQLite engine and a get_session generator function that FastAPI injects into each endpoint via Depends(), ensuring each request gets an isolated database session that is automatically closed after the response is sent. All 5 CRUD endpoints now use db.add(), db.commit(), db.refresh(), db.get(), and db.delete() instead of list operations, and data persists across server restarts in a tickets.db file on disk.
```
