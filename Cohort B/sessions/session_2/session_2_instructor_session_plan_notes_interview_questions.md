# Session 2 Instructor File: Add Database Layer + Data Modeling

## Session Title

Add Database Layer + Data Modeling

## Duration

2 hours

## Project

AI Support Ticket Resolution Copilot

## Session 2 Objective

By the end of Session 2, students should have replaced in-memory list storage with a persistent SQLite database using SQLModel. The Ticket model should be a proper SQLModel table with typed fields, timestamps, and an auto-increment primary key. All 5 CRUD endpoints should read from and write to the database. Data should survive a server restart.

This database layer becomes the persistent foundation for all future features:

- JWT authentication and per-user ticket ownership (Session 3)
- AI-powered ticket classification and summarization (Session 4)
- Semantic search with embeddings and ChromaDB (Session 5)
- LangGraph-based resolution agent (Session 6+)

## Session 2 Deliverable

Students will extend the Session 1 FastAPI project with:

1. A `Ticket` SQLModel table class with all required fields and proper types
2. A SQLite database engine and session factory using SQLModel
3. FastAPI dependency injection for the database session
4. All 5 CRUD endpoints updated to use database operations: `db.add`, `db.get`, `db.exec`, `db.delete`, `db.commit`, `db.refresh`
5. Table creation using `SQLModel.metadata.create_all(engine)` on startup
6. Data that persists across server restarts (verifiable by restarting uvicorn and querying GET /tickets)

## Strict Scope Control

### Include

- SQLite as the database (file-based, zero config)
- SQLModel for ORM (combines SQLAlchemy Core + Pydantic validation in one class)
- `Ticket` as a single SQLModel table with all fields: id, title, description, status, priority, created_at, updated_at
- `engine` created with `create_engine("sqlite:///./tickets.db")`
- `get_session` as a FastAPI dependency using `Session(engine)` as a context manager
- `SQLModel.metadata.create_all(engine)` called in a `startup` event or lifespan handler
- All 5 endpoints updated: POST /tickets, GET /tickets, GET /tickets/{id}, PUT /tickets/{id}, DELETE /tickets/{id}
- `db.add()`, `db.commit()`, `db.refresh()` for create
- `db.get(Ticket, ticket_id)` for single-record fetch
- `select(Ticket)` with `db.exec()` for list fetch
- Returning `HTTPException(status_code=404)` when a ticket is not found in the database
- Optional stretch: Alembic init and first migration (do not make this the main path)

### Do Not Include

- PostgreSQL (mention as a stretch/production option only — do not configure it)
- Async database sessions (`AsyncSession`, `async with`) — keep sync for clarity
- Multiple tables or relationships (e.g., User table, ForeignKey) — that comes in Session 3
- Redis, caching, or any queue
- Complex Alembic migration setup as the main path — use `create_all` in class
- `alembic upgrade head` as a required step for all students
- GraphQL or non-REST interfaces
- Field-level encryption or sensitive data handling (not yet)
- Pydantic v1 style validators (`@validator`) — use SQLModel's built-in field defaults

Session 2 is only about replacing in-memory storage with a working relational database layer.

---

# Instructor Framing

## Opening Message

In Session 1, we built a working FastAPI backend with 5 CRUD endpoints. Every ticket we created lived in a Python list in memory. That means every time uvicorn restarts, all tickets are gone. No real system works that way.

Today we replace that list with a real database. We will use SQLite as the database engine and SQLModel as our ORM. By the end of this session, every ticket will be stored in a file called `tickets.db`, and the data will survive server restarts, crashes, and redeploys.

This is the layer that makes the backend production-credible. Every feature we add after this — authentication, AI classification, vector search, agents — depends on tickets being reliably stored and retrievable.

## Key Philosophy

Students are not expected to memorize SQLAlchemy internals or SQL query syntax.

They are expected to:

- understand what an ORM does and why it matters
- read the SQLModel table definition and know what each field does
- understand the database session lifecycle (open, use, close)
- explain dependency injection for the DB session in FastAPI
- test persistence by restarting the server and calling GET /tickets
- debug the most common ORM errors (session not committed, 422 on missing fields, 404 for missing rows)
- explain the trade-offs between in-memory storage, SQLite, and PostgreSQL in interview language

## Repeated Instructor Line

The database layer is not optional infrastructure. It is the contract that every other feature in this system relies on.

---

# Session Flow

## 0–10 min: Opening and Recap of Session 1

### Instructor Goal

Establish continuity from Session 1 and frame the problem that today's feature solves.

### Recap Session 1 State

Open the existing codebase on screen. Show:

- `app/main.py` with the in-memory `tickets_db: list[dict]` variable
- the 5 existing endpoints: POST, GET (list), GET (by id), PUT, DELETE
- a quick demo: create a ticket in Swagger, then restart uvicorn, then call GET /tickets — show the empty response

### Ask Students

What is the problem with storing tickets in a Python list?

Expected answers:

- data is lost on restart
- cannot scale to multiple workers (each worker has its own list)
- no querying, filtering, or indexing
- no relationships possible

### Frame Today

Today we fix this by adding a SQLite database using SQLModel. By the end of this session, all 5 endpoints will read from and write to a `.db` file. The list disappears.

---

## 10–20 min: Architecture Breakdown — What Are We Adding and Why

### Instructor Goal

Show the full picture before any code is written. Students should understand what each new component does before AI generates it.

### Draw or Display This Flow

```
HTTP Request (POST /tickets)
        |
    FastAPI Route
        |
    Depends(get_session) --> DB Session opened
        |
    SQLModel ORM (Ticket object)
        |
    SQLite Engine (tickets.db file on disk)
        |
    DB Session closed (context manager)
        |
HTTP Response (201 Created)
```

### Explain Each Layer

1. **SQLite**: A file on disk (`tickets.db`). No separate server process. Perfect for development and low-traffic production. The full database lives in one file.
2. **SQLModel**: A Python library that lets you define a class (`Ticket`) that is simultaneously a Pydantic model (for request/response validation) and a SQLAlchemy table (for database operations). One class does both jobs.
3. **Engine**: The connection object. Created once at app startup using `create_engine()`. Manages the connection pool.
4. **Session**: A unit of work against the database. Opened per request, used for operations, then closed. Never share sessions across requests.
5. **Dependency injection**: FastAPI's `Depends(get_session)` mechanism injects a fresh session into each endpoint function. The session is automatically closed after the request completes.

### Key Question for Students

Why not just use raw SQL queries with the `sqlite3` module?

Expected answer: raw SQL works but gives you no type safety, no Python object model, no validation, and no migration tooling. ORM is the right abstraction for an application-level backend.

---

## 20–35 min: Build the Feature Using Antigravity

### Instructor Goal

Run the main build prompt and generate the database layer. The instructor should run this live on screen.

### Before Running the Prompt

Check that the Session 1 codebase is in the expected state:

- `app/main.py` exists with in-memory list
- `app/models.py` exists with Pydantic `TicketCreate` and `TicketResponse` models
- `requirements.txt` exists with `fastapi`, `uvicorn`, `pydantic`

### Run Prompt 1 (Main Build Prompt) from the Student Pre-Session File

Paste the prompt into Antigravity. Observe what is generated.

### What to Watch For in the Generated Code

- Is `Ticket` defined with `table=True` in the SQLModel class?
- Is `id` defined as `Optional[int] = Field(default=None, primary_key=True)`?
- Is `created_at` using `datetime` with `default_factory=datetime.utcnow`?
- Is `get_session` a generator function using `yield`?
- Is `create_all` called somewhere on startup?
- Are all 5 endpoints updated, not just some of them?
- Is `db.commit()` followed by `db.refresh()` after create?

### Instructor Control Rule

Do not let students run the prompt until the instructor has reviewed the generated output on screen. Ensure the generated code is correct before the class builds it.

---

## 35–50 min: Instructor Code Walkthrough

### Instructor Goal

Every student should understand the generated code before they build it themselves. Read and explain each file.

### Walk Through `app/models.py` or `app/db/models.py`

```python
from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime

class Ticket(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str
    description: str
    status: str = Field(default="open")
    priority: str = Field(default="medium")
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
```

Explain:
- `table=True` is what makes this a database table, not just a Pydantic model
- `Optional[int]` on `id` — it is None before the row is inserted, then SQLite assigns it
- `Field(primary_key=True)` — tells SQLAlchemy this is the primary key column
- `default_factory=datetime.utcnow` — evaluated at insert time, not at class definition time
- fields without defaults (`title`, `description`) are required

### Walk Through `app/db/database.py`

```python
from sqlmodel import create_engine, Session, SQLModel

DATABASE_URL = "sqlite:///./tickets.db"
engine = create_engine(DATABASE_URL, echo=True)

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

def get_session():
    with Session(engine) as session:
        yield session
```

Explain:
- `create_engine` creates the connection. `echo=True` prints SQL to stdout — useful for debugging, remove in production
- `SQLModel.metadata.create_all(engine)` reads all classes with `table=True` and creates the corresponding tables if they do not exist — idempotent, safe to call on startup
- `get_session` is a generator. The `yield` is the hand-off point. FastAPI receives the session, injects it into the endpoint, then continues after the `with` block closes — which closes the session

### Walk Through an Updated Endpoint

```python
@app.post("/tickets", response_model=TicketResponse, status_code=201)
def create_ticket(ticket: TicketCreate, db: Session = Depends(get_session)):
    db_ticket = Ticket.model_validate(ticket)
    db.add(db_ticket)
    db.commit()
    db.refresh(db_ticket)
    return db_ticket
```

Explain:
- `Ticket.model_validate(ticket)` converts the Pydantic input model to a SQLModel instance
- `db.add()` stages the object — no SQL has run yet
- `db.commit()` flushes the transaction and writes to disk
- `db.refresh()` re-reads the row from the database, populating auto-generated fields like `id` and `created_at`

### Ask During Walkthrough

- What happens if we forget `db.commit()`?
- What happens if we call `db.refresh()` before `db.commit()`?
- Why is `id` typed as `Optional[int]` rather than `int`?
- What does `Depends(get_session)` actually do?

---

## 50–65 min: Student Follow-Along Build

### Student Task

Students run Prompt 1 from the pre-session file in their own Antigravity environment. They should have the Session 1 codebase already open.

### Instructor Support Areas

Help students with:

- `ModuleNotFoundError: No module named 'sqlmodel'` — run `pip install sqlmodel`
- `sqlalchemy.exc.OperationalError: table tickets already exists` — `create_all` is idempotent, this should not happen, but if it does, delete `tickets.db` and restart
- `422 Unprocessable Entity` on POST — field names in the request body do not match the model
- `AttributeError: 'NoneType' object has no attribute 'title'` — `db.get()` returned `None`, means the ticket does not exist; needs a 404 guard
- Endpoint returns data but `tickets.db` file is not created — `create_db_and_tables()` was not called on startup

### If Student Build Fails

Do not block the class. The student follows along on the instructor screen. Share the completed code after class. Do not sacrifice the interview explanation section at the end.

---

## 65–80 min: Test and Verify Persistence

### Instructor Goal

Prove that the feature works AND that it actually persists across restarts. This is the core value proposition of Session 2.

### Test Sequence in Swagger (http://127.0.0.1:8000/docs)

1. POST /tickets — create a ticket with title, description, priority
2. GET /tickets — confirm the ticket appears with an auto-assigned `id` and `created_at`
3. GET /tickets/{id} — confirm single-ticket fetch works
4. PUT /tickets/{id} — update the status to "in_progress", confirm response
5. DELETE /tickets/{id} — confirm 204 No Content response
6. POST /tickets — create 2 more tickets
7. **Stop the uvicorn server** (`Ctrl+C` in terminal)
8. **Restart uvicorn**: `uvicorn app.main:app --reload`
9. GET /tickets — confirm the 2 tickets are still there

Step 7-9 is the proof. If the GET returns tickets after restart, the database layer works.

### Also Check

- Open `tickets.db` in DB Browser for SQLite or run `sqlite3 tickets.db "SELECT * FROM ticket;"` in terminal — students should see their rows

### Instructor Explanation

This is why we do not use in-memory storage in production. Any restart, crash, or horizontal scale event would wipe the state. The database is the single source of truth.

---

## 80–95 min: Error Handling and Edge Cases

### Instructor Goal

Make the endpoints production-credible by handling the cases that the happy-path build ignores.

### Add These Guards

**GET /tickets/{id} — ticket not found**

```python
ticket = db.get(Ticket, ticket_id)
if not ticket:
    raise HTTPException(status_code=404, detail="Ticket not found")
return ticket
```

**PUT /tickets/{id} — partial update pattern**

```python
ticket = db.get(Ticket, ticket_id)
if not ticket:
    raise HTTPException(status_code=404, detail="Ticket not found")
ticket_data = ticket_update.model_dump(exclude_unset=True)
for key, value in ticket_data.items():
    setattr(ticket, key, value)
ticket.updated_at = datetime.utcnow()
db.add(ticket)
db.commit()
db.refresh(ticket)
return ticket
```

Explain `exclude_unset=True` — only updates fields the client explicitly sent, does not overwrite fields with None.

**DELETE /tickets/{id} — ticket not found**

```python
ticket = db.get(Ticket, ticket_id)
if not ticket:
    raise HTTPException(status_code=404, detail="Ticket not found")
db.delete(ticket)
db.commit()
return Response(status_code=204)
```

### What to Emphasize

Every endpoint that takes an ID from the URL must check whether the row exists. Never assume the database has the row. Always guard with a 404.

---

## 95–105 min: Concept Pause — Database Modeling, ORM, and Persistence

### Instructor Goal

Convert implementation into interview-ready understanding.

### Explain the Core Trade-Offs

**In-Memory vs SQLite vs PostgreSQL**

| Factor | In-Memory (list) | SQLite | PostgreSQL |
|---|---|---|---|
| Persistence | No | Yes (file) | Yes (server) |
| Concurrent writes | Unsafe | Limited (file lock) | Full ACID |
| Setup complexity | Zero | Zero | Medium-High |
| Production-ready | No | Low-traffic yes | Yes |
| Horizontal scaling | Breaks | Breaks | Yes (with pooler) |

SQLite is the right choice for development and low-traffic single-server deployments. When you need concurrent writes from multiple workers, you move to PostgreSQL.

**What an ORM does**

An ORM maps Python classes to database tables. It handles SQL generation, connection management, type coercion, and transaction management. The trade-off: you give up fine-grained SQL control for developer speed and type safety. For a CRUD API, ORM is almost always the right choice.

**SQLModel vs raw SQLAlchemy vs plain SQL**

- Raw SQL: maximum control, zero abstraction, no type safety
- Raw SQLAlchemy: full ORM power, verbose model definition, separate Pydantic schema needed
- SQLModel: combines SQLAlchemy + Pydantic into one class definition — ideal for FastAPI projects where you want one source of truth for both the database schema and the API schema

### Student Writing Task

Ask every student to write a 2–3 line answer:

What is the difference between `db.add()`, `db.commit()`, and `db.refresh()`?

Expected answer: `db.add()` stages the object in the session's unit-of-work queue. `db.commit()` flushes all staged changes as a transaction to the database. `db.refresh()` re-reads the row from the database to populate auto-generated fields like `id` and `created_at` that were set by SQLite, not by Python.

---

## 105–115 min: Interview Discussion and Technical Viva Practice

### Instructor Goal

Prepare students to speak about this feature at a technical level.

Use the interview questions section below. Run 5–7 questions as a class viva. Call on students by name. For questions they miss, give the answer and have them repeat it.

---

## 115–120 min: Wrap-Up and Session 3 Preview

### Instructor Closing

Today we replaced in-memory storage with a real SQLite database using SQLModel. Every ticket is now stored in `tickets.db`. Data survives restarts. All 5 endpoints talk to the database through a managed session.

In Session 3, we will add JWT-based authentication and role-based access control. We will add a User table, a login endpoint, and protect the ticket endpoints so only authenticated users can create or modify tickets. The database layer we built today is what makes user ownership of tickets possible.

---

# Instructor Notes

## What to Emphasize

Session 2 is about persistence and correctness. The two things to hammer on:

1. Why in-memory storage is not acceptable in any real backend — use the restart demo as the proof
2. What each ORM operation does — students must be able to explain `add`, `commit`, `refresh`, `get`, `exec`, `delete` in their own words, not just copy the pattern

The session success criterion is: student restarts uvicorn and GET /tickets still returns data.

## Common Student Mistakes

1. **Forgetting `table=True`**: Defining `class Ticket(SQLModel)` without `table=True` creates a Pydantic-only model. The table is never created in the database. Error is silent — `create_all` runs but creates nothing. Fix: add `table=True`.

2. **Forgetting `db.commit()`**: After `db.add()`, the student checks the response and sees the ticket with an ID. But the ID is a SQLAlchemy-generated placeholder, not a committed row. After restart, the row does not exist. Always `commit()` after mutations.

3. **Forgetting `db.refresh()` after commit**: The `id` field shows as `None` in the response even though it was committed. SQLite assigned the ID, but the Python object was not refreshed to read it back. Fix: `db.refresh(db_ticket)` after `db.commit()`.

4. **Importing `Session` from `sqlalchemy.orm` instead of `sqlmodel`**: This causes type errors because the SQLModel `Session` has additional methods. Always import from `sqlmodel`: `from sqlmodel import Session`.

5. **422 on POST /tickets**: Usually because the request body field names do not match the model field names. For example, sending `"ticket_title"` when the model has `title`. Check the Pydantic model and the request body carefully.

6. **`AttributeError: 'NoneType' object has no attribute 'title'`**: Student calls `db.get(Ticket, ticket_id)` and uses the return value without checking for `None`. Any GET/PUT/DELETE by ID must guard with `if not ticket: raise HTTPException(404)`.

7. **`sqlalchemy.exc.OperationalError: no such table: ticket`**: `create_db_and_tables()` was not called at startup, or was called before the `Ticket` model was imported. Fix: ensure `from app.models import Ticket` is imported before `create_all` is called.

8. **Session not closed — `ResourceWarning: unclosed <ssl.SSLSocket>`**: Student is not using `get_session` as a dependency but is creating `Session(engine)` directly in the endpoint without a `with` block or explicit `close()`. Fix: always use `Depends(get_session)` with the generator pattern.

9. **`updated_at` not updating on PUT**: Student copies the create logic but does not manually set `ticket.updated_at = datetime.utcnow()` in the update endpoint. The `default_factory` only fires on row creation. Fix: explicitly set `updated_at` in the update handler.

10. **`tickets.db` file in wrong directory**: The engine is created with `sqlite:///./tickets.db` which creates the file relative to the current working directory at startup. If uvicorn is run from a different directory than expected, the file path is wrong. Fix: always run uvicorn from the project root.

## How to Control the Session

Use this rule:

If a proposed addition is not required for the 5 endpoints to persist tickets to SQLite, do not add it this session.

Common scope creep to watch for:
- Students wanting to add a `User` table — that is Session 3
- Students wanting to switch to PostgreSQL — that is an optional stretch, do not configure it in class
- Students wanting to add Alembic migrations as the primary path — use `create_all` for Session 2, mention Alembic as a professional tool to add later
- Students wanting to add async sessions — out of scope, adds complexity without benefit at this stage

## Setup Rule

Do not spend more than 5 minutes on package installation in live class.

Run `pip install sqlmodel` before the session starts. If a student's environment is broken, they follow along and fix after class.

---

# Questions to Discuss: Interview Perspective

## Basic Project Questions

### Q1. What change did you make in Session 2?

Expected answer:

In Session 2 we replaced the in-memory Python list that was storing tickets with a persistent SQLite database. We used SQLModel as the ORM to define a `Ticket` table class. We added a database engine, a session factory with dependency injection, and updated all 5 CRUD endpoints to use database operations. The key validation of the change was restarting uvicorn and confirming that GET /tickets still returned the previously created tickets — proving that data now persists across server restarts.

### Q2. What is SQLModel and why did you use it instead of raw SQLAlchemy?

Expected answer:

SQLModel is a Python library built on top of SQLAlchemy and Pydantic. It allows a single class definition to serve as both the database table schema and the API request/response validation schema. In a plain SQLAlchemy + FastAPI project, you typically write two separate classes: a SQLAlchemy `Table` or declarative `Base` model and a Pydantic schema. SQLModel collapses these into one class with `table=True`. This reduces duplication and keeps the data contract in a single source of truth. For a FastAPI-based backend where every model is both persisted and serialized, SQLModel is the most ergonomic choice.

### Q3. What is a database session and why does each request get its own session?

Expected answer:

A database session is a unit of work that represents a connection to the database for the duration of a single operation or transaction. It tracks all objects that have been added, modified, or deleted within that unit of work. Each request gets its own session because database sessions are not thread-safe and are not meant to be shared. If two concurrent requests shared a session, their transactions could interfere — for example, one request committing changes that the other request has not finished preparing. The FastAPI dependency `Depends(get_session)` creates a new session at the start of each request and closes it after the response is sent, ensuring clean isolation.

### Q4. What is the purpose of `SQLModel.metadata.create_all(engine)`?

Expected answer:

`SQLModel.metadata.create_all(engine)` inspects all Python classes that have been defined with `SQLModel, table=True` and issues `CREATE TABLE IF NOT EXISTS` SQL statements for each one. It is idempotent — calling it multiple times will not drop and recreate tables or lose data. It is the simplest way to initialize the database schema for a new project. In production, you would replace this with Alembic migrations to handle schema changes without data loss, but for development and the early build stages of this project, `create_all` is the correct and safe choice.

### Q5. Why did you choose SQLite and what are its limitations?

Expected answer:

We chose SQLite because it requires zero setup — the database is a single file on disk, there is no separate server process to start or configure, and it is bundled with Python's standard library. For development and single-server deployments with low write concurrency, SQLite is entirely adequate. Its key limitation is write concurrency: SQLite uses file-level locking, so only one write transaction can occur at a time. If you run FastAPI with multiple uvicorn workers, concurrent writes will fail with `OperationalError: database is locked`. For production systems that need horizontal scaling or high write throughput, you would switch to PostgreSQL, which supports full ACID transactions with row-level locking and concurrent connections.

---

## Technical Deep-Dive Questions

### Q6. Walk me through what happens when POST /tickets is called, from HTTP request to database row.

Expected answer:

The HTTP request arrives with a JSON body. FastAPI deserializes it into a `TicketCreate` Pydantic model, validating field types and required fields. If validation fails, FastAPI returns a 422 before the endpoint function runs. If validation passes, the endpoint function is invoked with a fresh `Session` injected by `Depends(get_session)`. Inside the function, `Ticket.model_validate(ticket)` converts the Pydantic input into a SQLModel `Ticket` instance. `db.add(db_ticket)` stages the object in the session's unit of work. `db.commit()` issues an `INSERT INTO ticket (title, description, status, priority, created_at, updated_at) VALUES (...)` SQL statement and commits the transaction. `db.refresh(db_ticket)` issues a `SELECT * FROM ticket WHERE id = ?` to reload the row, populating the auto-incremented `id` that SQLite assigned. The endpoint returns the `db_ticket` object, which FastAPI serializes to JSON using the `TicketResponse` schema and returns with HTTP 201.

### Q7. What is the difference between `db.add()`, `db.commit()`, and `db.refresh()`?

Expected answer:

`db.add(obj)` places the SQLModel object into the session's identity map and marks it as pending. No SQL is sent to the database at this point. `db.commit()` flushes all pending operations in the session — inserts, updates, deletes — as a single atomic transaction. The SQL statements are compiled and sent to the database, and the transaction is committed to disk. `db.refresh(obj)` issues a fresh `SELECT` query for the specific row and updates the Python object with the current state from the database. This is necessary after an insert because the database may have assigned auto-generated values — the primary key, default timestamps, or any server-side computed columns — that are not reflected in the in-memory Python object until a refresh is performed.

### Q8. Why is `id` typed as `Optional[int]` in the Ticket model rather than just `int`?

Expected answer:

Before a `Ticket` instance is inserted into the database, its `id` is `None`. SQLite assigns the auto-increment integer primary key at insert time, not at object construction time. If `id` were typed as a non-optional `int`, Pydantic would require a value at model instantiation — you would have to invent a fake ID before the row exists in the database, which is incorrect. Typing it as `Optional[int] = Field(default=None, primary_key=True)` correctly expresses the lifecycle: the field is nullable during construction, SQLite fills it in on insert, and `db.refresh()` populates the Python object with the assigned value. After a successful commit and refresh, `ticket.id` is always an integer; the optionality is an artifact of the pre-insert lifecycle.

### Q9. How does FastAPI's `Depends(get_session)` work, and what happens if the endpoint raises an exception?

Expected answer:

`get_session` is a generator function that uses `with Session(engine) as session: yield session`. When FastAPI resolves the `Depends(get_session)` dependency for a request, it calls the generator and runs it up to the `yield`, receiving the session object. It injects that session into the endpoint function. After the endpoint function returns — whether normally or by raising an exception — FastAPI continues running the generator past the `yield` point, which triggers the `with` block's `__exit__`, closing the session. If the endpoint raised an exception without calling `db.commit()`, the session is closed with no commit, so the transaction is automatically rolled back. This means exceptions during a request will never leave the database in a partially-written state, which is the correct behavior for a transactional system.

### Q10. What is `exclude_unset=True` in the PUT endpoint and why does it matter?

Expected answer:

`model_dump(exclude_unset=True)` returns a dictionary containing only the fields that the client explicitly included in the request body, excluding any fields that were not set and therefore have their default values. In a PATCH-style partial update, the client may only want to update `status` without changing `title` or `description`. Without `exclude_unset=True`, `model_dump()` would return all fields, including `title` with a `None` or default value, and `setattr(ticket, 'title', None)` would overwrite the existing title with `None`. With `exclude_unset=True`, only `{"status": "in_progress"}` is returned, and only the `status` field is updated on the object. This is the correct pattern for partial update endpoints and prevents accidental data loss.

---

## System Design and Trade-Off Questions

### Q11. When would you move from SQLite to PostgreSQL in this project, and what changes would that require?

Expected answer:

The migration to PostgreSQL is warranted when any of these conditions arise: you need to run multiple uvicorn workers (SQLite's file lock breaks under concurrent writes), you need to deploy to a cloud environment where the filesystem is ephemeral (Heroku dynos, Railway, Fly.io restart destroy the `tickets.db` file), or you need full ACID compliance with row-level locking for high write throughput. The code changes are minimal — SQLModel abstracts the database dialect. You would change `DATABASE_URL = "sqlite:///./tickets.db"` to `DATABASE_URL = "postgresql://user:password@host/dbname"`, install `psycopg2` or `asyncpg`, remove `connect_args={"check_same_thread": False}` from the engine, and configure a connection pool with `pool_size` and `max_overflow`. The SQLModel table definitions and all endpoint code remain unchanged. The primary operational change is managing the PostgreSQL server or connecting to a managed cloud database.

### Q12. What are the trade-offs between using an ORM like SQLModel versus writing raw SQL queries?

Expected answer:

The ORM approach gives you type safety, Python-native object manipulation, automatic SQL generation, and integration with Pydantic for request/response validation. It reduces the risk of SQL injection because parameters are always escaped by the ORM. It speeds up development significantly for standard CRUD operations. The trade-offs are: ORM-generated queries can be inefficient for complex operations — for example, an ORM might execute N+1 queries where a single JOIN would suffice, or generate a suboptimal query plan that a raw SQL author would write better. For a CRUD API like this ticket system, the ORM is clearly the right choice. For a reporting system executing complex analytical queries across large datasets, raw SQL or a query builder like SQLAlchemy Core expressions would give better performance control.

### Q13. What is a database migration and when would you use Alembic instead of `create_all`?

Expected answer:

A database migration is a versioned, reversible script that describes a schema change — adding a column, dropping a table, creating an index. Alembic is the standard migration tool for SQLAlchemy-based projects. `SQLModel.metadata.create_all(engine)` only creates tables that do not exist yet. It cannot add a column to an existing table, rename a column, or drop a constraint. If you change the `Ticket` model in Session 3 — for example, adding a `user_id` foreign key column — `create_all` will not apply that change to the existing database. Alembic tracks which migrations have been applied and can upgrade or downgrade the schema incrementally. In production, where you cannot drop the database between deploys, Alembic is mandatory. For the early sessions of this project, `create_all` is acceptable because the schema is new and there is no production data to protect.

### Q14. How does the session lifecycle relate to database transactions, and what happens if you forget to call `db.commit()`?

Expected answer:

Every SQLModel session operates within a transaction. When you call `db.add()` and then `db.commit()`, the session issues a `BEGIN` statement (implicitly in SQLite, explicitly in PostgreSQL), sends the `INSERT` or `UPDATE` SQL, and then issues `COMMIT`. If you call `db.add()` but forget `db.commit()` before the session closes, the session's `__exit__` method is called, which issues a `ROLLBACK`. The data never reaches the disk. The endpoint function may return a successful response with what appears to be a valid ticket object — including a placeholder ID from SQLAlchemy's identity map — but after the session closes and the next request queries the database, that row does not exist. This is one of the most confusing bugs in ORM-based development: the endpoint returns 201, the response body looks correct, but the data is not in the database.

### Q15. How does dependency injection for the database session fit into the broader FastAPI architecture, and what would happen if you created the session as a module-level global instead?

Expected answer:

A module-level global session would be a single `Session(engine)` instance shared across all requests. This breaks in multiple ways: SQLAlchemy sessions are not thread-safe, so concurrent requests would corrupt each other's transactions. A long-running session accumulates an identity map of loaded objects, consuming memory. If one request's transaction fails and rolls back, it could invalidate the session state for other requests using the same session. FastAPI's dependency injection with a generator function solves all of these: each request gets a fresh session, the session is scoped to the request lifetime, and it is automatically closed when the request completes. The `Depends` mechanism also makes the session mockable in tests — you can override `get_session` in the test client to inject an in-memory SQLite session for isolation, which is exactly the pattern used in the pytest tests we write later.

---

# Session 2 Completion Checklist

Students should verify all of the following by the end of the session:

- [ ] `pip install sqlmodel` completed without errors and `import sqlmodel` works in Python shell
- [ ] `Ticket` class defined with `table=True`, all required fields, correct types, and `Optional[int]` primary key
- [ ] `created_at` and `updated_at` fields use `default_factory=datetime.utcnow`, not `default=datetime.utcnow()`
- [ ] `engine` created with `create_engine("sqlite:///./tickets.db")` and `create_db_and_tables()` called at startup
- [ ] `get_session` is a generator function using `with Session(engine) as session: yield session`
- [ ] All 5 endpoints updated to accept `db: Session = Depends(get_session)` and use database operations
- [ ] Swagger POST /tickets returns HTTP 201 with an auto-assigned integer `id` in the response body
- [ ] Swagger GET /tickets returns a list of all tickets from the database
- [ ] Swagger GET /tickets/{id} returns 200 for an existing ticket and 404 for a non-existent ID
- [ ] Swagger PUT /tickets/{id} updates the ticket and returns the updated fields including `updated_at`
- [ ] Swagger DELETE /tickets/{id} returns 204 and the ticket no longer appears in GET /tickets
- [ ] Server is restarted (`Ctrl+C` + `uvicorn app.main:app --reload`) and previously created tickets are still returned by GET /tickets

---

# Instructor Backup Plan

If Antigravity generation fails or produces incorrect output:

1. Instructor switches to pre-written reference code and pastes it file by file on screen.
2. Students copy the reference code directly — understanding walk-through still happens for all files.
3. Share the completed Session 2 codebase with students after class via the shared repository.
4. Students use Prompt 2 (improvement) and Prompt 3 (debugging) to practice with AI on the working codebase.
5. Do not sacrifice the concept pause (95–105 min) or the interview questions section. These are the highest-value parts of the session for interview preparation.
6. If the `tickets.db` file cannot be created due to filesystem permissions (rare on macOS/Windows), switch the DATABASE_URL to `"sqlite:///:memory:"` for the session demo and explain the difference — data will not persist but all ORM operations will work correctly for walkthrough purposes.
